# Copyright 2012 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Basic locking functionality."""

import contextlib
import errno
import fcntl
import logging
import os
import stat
import tempfile
from typing import Optional

from chromite.lib import cros_build_lib
from chromite.lib import osutils
from chromite.lib import retry_util
from chromite.lib import timeout_util


LOCKF = "lockf"
FLOCK = "flock"


class LockNotAcquiredError(Exception):
    """Signals that the lock was not acquired."""


class LockingError(Exception):
    """Signals miscellaneous problems in the locking process."""


@contextlib.contextmanager
def _optional_timer_context(timeout):
    """Use the timeout_util.Timeout contextmanager if timeout is set."""
    if timeout:
        with timeout_util.Timeout(timeout):
            yield
    else:
        yield


class _Lock(cros_build_lib.PrimaryPidContextManager):
    """Base lockf based locking.  Derivatives need to override _GetFd"""

    def __init__(
        self,
        description=None,
        verbose=True,
        locktype=LOCKF,
        blocking=True,
        blocking_timeout=None,
    ) -> None:
        """Initialize this instance.

        Two types of locks are available: LOCKF and FLOCK.

        Use LOCKF (POSIX locks) if:
          - you need to lock a file between processes created by the
            parallel/multiprocess libraries

        Use FLOCK (BSD locks) if these scenarios apply:
          - you need to lock a file between shell scripts running the flock
            program
          - you need the lock to be bound to the fd and thus inheritable across
            execs

        Note: These two locks are completely independent; using one on a path
            will not block using the other on the same path.

        Args:
            path: On disk pathway to lock.  Can be a directory or a file.
            description: A description for this lock- what is it protecting?
            verbose: Verbose logging?
            locktype: Type of lock to use (lockf or flock).
            blocking: If True, use a blocking lock.
            blocking_timeout: If not None, time is seconds to wait on blocking
                calls.
        """
        cros_build_lib.PrimaryPidContextManager.__init__(self)
        self._verbose = verbose
        self.description = description
        self._fd = None
        if locktype == FLOCK:
            self.locking_mechanism = fcntl.flock
        else:
            self.locking_mechanism = fcntl.lockf
        self.locktype = locktype
        self.blocking = blocking
        self.blocking_timeout = blocking_timeout

    @property
    def fd(self):
        if self._fd is None:
            self._fd = self._GetFd()
            # Ensure that all derivatives of this lock can't bleed the fd
            # across execs.
            fcntl.fcntl(
                self._fd,
                fcntl.F_SETFD,
                fcntl.fcntl(self._fd, fcntl.F_GETFD) | fcntl.FD_CLOEXEC,
            )
        return self._fd

    def _GetFd(self) -> None:
        raise NotImplementedError(self, "_GetFd")

    def _enforce_lock(self, flags, message) -> None:
        # Try nonblocking first, if it fails, display the context/message,
        # and then wait on the lock.
        try:
            self.locking_mechanism(self.fd, flags | fcntl.LOCK_NB)
            return
        except EnvironmentError as e:
            if e.errno == errno.EDEADLK:
                self.unlock()
            elif e.errno != errno.EAGAIN:
                raise
        if self.description:
            message = "%s: blocking (LOCK_NB) (%s) while %s" % (
                self.description,
                self.locktype,
                message,
            )
        if not self.blocking:
            self.close()
            raise LockNotAcquiredError(message)
        if self._verbose:
            logging.info(message)

        try:
            with _optional_timer_context(self.blocking_timeout):
                self.locking_mechanism(self.fd, flags)
        except timeout_util.TimeoutError:
            description = self.description or "locking._enforce_lock"
            logging.error(
                "Timed out after waiting %d seconds for blocking lock (%s): %s",
                self.blocking_timeout,
                self.locktype,
                description,
            )
            raise
        except EnvironmentError as e:
            if e.errno != errno.EDEADLK:
                logging.error(
                    "%s: blocking wait failed errno %s", self.description, e
                )
                raise
            self.unlock()
            self.locking_mechanism(self.fd, flags)

    def lock(self, shared=False):
        """Take a lock of type |shared|.

        Any existing lock will be updated if need be.

        Args:
            shared: If True make the lock shared.

        Returns:
            self, allowing it to be used as a `with` target.

        Raises:
            IOError if the operation fails in some way.
            LockNotAcquiredError if the lock couldn't be acquired (non-blocking
            mode only).
        """
        self._enforce_lock(
            fcntl.LOCK_SH if shared else fcntl.LOCK_EX,
            "taking a %s lock" % ("shared" if shared else "exclusive"),
        )
        return self

    def read_lock(self, message="taking read lock"):
        """Take a read lock (shared), downgrading from write if required.

        Args:
            message: A description of what/why this lock is being taken.

        Returns:
            self, allowing it to be used as a `with` target.

        Raises:
            IOError if the operation fails in some way.
        """
        self._enforce_lock(fcntl.LOCK_SH, message)
        return self

    def write_lock(self, message="taking write lock"):
        """Take a write lock (exclusive), upgrading from read if required.

        Note that if the lock state is being upgraded from read to write,
        a deadlock potential exists- as such we *will* release the lock
        to work around it.  Any consuming code should not assume that
        transitioning from shared to exclusive means no one else has
        gotten at the critical resource in between for this reason.

        Args:
            message: A description of what/why this lock is being taken.

        Returns:
            self, allowing it to be used as a `with` target.

        Raises:
            IOError if the operation fails in some way.
        """
        self._enforce_lock(fcntl.LOCK_EX, message)
        return self

    def unlock(self) -> None:
        """Release any locks held.  Noop if no locks are held.

        Raises:
            IOError if the operation fails in some way.
        """
        if self._fd is not None:
            self.locking_mechanism(self._fd, fcntl.LOCK_UN)

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        """Release the underlying lock and close the fd."""
        if self._fd is not None:
            self.unlock()
            os.close(self._fd)
            self._fd = None

    def _enter(self):
        # Force the fd to be opened via touching the property. We do this to
        # ensure that even if entering a context w/out a lock held, we can do
        # locking in that critical section if the code requests it.
        # pylint: disable=pointless-statement
        self.fd
        return self

    def _exit(self, exc_type, exc, exc_tb) -> None:
        try:
            self.unlock()
        finally:
            self.close()

    def IsLocked(self):
        """Return True if the lock is grabbed."""
        return bool(self._fd)


class FileLock(_Lock):
    """Use a specified file as a locking mechanism."""

    def __init__(
        self,
        path,
        description=None,
        verbose=True,
        locktype=LOCKF,
        world_writable=False,
        blocking=True,
        blocking_timeout=None,
    ) -> None:
        """Initializer for FileLock.

        Args:
            path: On disk pathway to lock.  Can be a directory or a file.
            description: A description for this lock- what is it protecting?
            verbose: Verbose logging?
            locktype: Type of lock to use (lockf or flock).
            world_writable: If true, the lock file will be created as root and
                be made writable to all users.
            blocking: If True, use a blocking lock.
            blocking_timeout: If not None, time is seconds to wait on blocking
                calls.
        """
        if description is None:
            description = "lock %s" % (path,)
        _Lock.__init__(
            self,
            description=description,
            verbose=verbose,
            locktype=locktype,
            blocking=blocking,
            blocking_timeout=blocking_timeout,
        )
        self.path = os.path.abspath(path)
        self.world_writable = world_writable

    def _GetFd(self):
        if self.world_writable:
            create = True
            try:
                create = stat.S_IMODE(os.stat(self.path).st_mode) != 0o666
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise
            if create:
                osutils.SafeMakedirs(os.path.dirname(self.path), sudo=True)
                cros_build_lib.sudo_run(["touch", self.path], print_cmd=False)
                cros_build_lib.sudo_run(
                    ["chmod", "666", self.path], print_cmd=False
                )

        # There exist race conditions where the lock may be created by
        # root, thus denying subsequent accesses from others. To prevent
        # this, we create the lock with mode 0o666.
        with osutils.UmaskContext(000):
            return os.open(
                self.path, os.W_OK | os.O_CREAT | os.O_CLOEXEC, 0o666
            )


class ProcessLock(_Lock):
    """Process level locking visible to parent/child only.

    This lock is basically a more robust version of what
    multiprocessing.Lock does.  That implementation uses semaphores
    internally which require cleanup/deallocation code to run to release
    the lock; a SIGKILL hitting the process holding the lock violates those
    assumptions leading to a stuck lock.

    Thus this implementation is based around locking of a deleted tempfile;
    lockf locks are guranteed to be released once the process/fd is closed.
    """

    def _GetFd(self):
        with tempfile.TemporaryFile() as f:
            # We don't want to hold onto the object indefinitely; we just want
            # the fd to a temporary inode, preferably one that isn't vfs
            # accessible. Since TemporaryFile closes the fd once the object is
            # GC'd, we just dupe the fd so we retain a copy, while the original
            # TemporaryFile goes away.
            return os.dup(f.fileno())


class PortableLinkLock:
    """A more primitive lock that relies on the atomicity of creating hardlinks.

    Use this lock if you need to be compatible with shadow utils like groupadd
    or useradd.
    """

    def __init__(self, path, max_retry=0, sleep=1) -> None:
        """Construct an instance.

        Args:
            path: path to file to lock on.  Multiple processes attempting to
                lock the same path will compete for a system-wide lock.
            max_retry: maximum number of times to attempt to acquire the lock.
            sleep: See retry_util.GenericRetry's sleep parameter.
        """
        self._path = path
        self._target_path = None
        # These two poorly named variables are just passed straight through to
        # retry_util.RetryException.
        self._max_retry = max_retry
        self._sleep = sleep

    def __enter__(self):
        fd, self._target_path = tempfile.mkstemp(
            prefix=self._path + ".chromite.portablelock."
        )
        os.close(fd)
        try:
            retry_util.RetryException(
                OSError,
                self._max_retry,
                os.link,
                self._target_path,
                self._path,
                sleep=self._sleep,
            )
        except OSError:
            raise LockNotAcquiredError(
                "Timeout while trying to lock %s" % self._path
            )
        finally:
            osutils.SafeUnlink(self._target_path)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if self._target_path:
                osutils.SafeUnlink(self._target_path)
        finally:
            osutils.SafeUnlink(self._path)


class PipeLock:
    """A simple one-way lock based on pipe().

    This is used when code is calling os.fork() directly and needs to
    synchronize behavior between the two.  The same process must not try to
    use both Wait and Post.  If you need bidirectional locks, you'll need to
    create two yourself.

    Be sure to delete the lock when you're done to prevent fd leakage.
    """

    def __init__(self) -> None:
        self._read_fd: Optional[int]
        self._write_fd: Optional[int]
        self._read_fd, self._write_fd = os.pipe2(os.O_CLOEXEC)

    def Wait(self, size: int = 1) -> bytes:
        """Read |size| bytes from the pipe.

        Args:
            size: How many bytes to read.  It must match the length of |data|
                passed by the other end during its call to Post.

        Returns:
            The data read back.  Note that this will be shorter than requested
            if the other end closed the lock (e.g., early termination).
        """
        # We've chosen to use the "read" end of the pipe; close the "write" end.
        if self._write_fd is not None:
            os.close(self._write_fd)
            self._write_fd = None

        assert self._read_fd is not None
        return os.read(self._read_fd, size)

    def Post(self, data: bytes = b"!") -> None:
        """Write |data| to the pipe.

        Args:
            data: The data to send to the other side calling Wait.  It must be
                of the exact length that is passed to Wait.
        """
        # We've chosen to use the "write" end of the pipe; close the "read" end.
        if self._read_fd is not None:
            os.close(self._read_fd)
            self._read_fd = None

        assert self._write_fd is not None
        try:
            os.write(self._write_fd, data)
        except BrokenPipeError:
            # Other end is all closed up. That's OK.
            pass

    def __del__(self) -> None:
        if self._read_fd is not None:
            os.close(self._read_fd)
        if self._write_fd is not None:
            os.close(self._write_fd)
