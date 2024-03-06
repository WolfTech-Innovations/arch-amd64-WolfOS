# Copyright (c) 2018 The Fyde OS Authors. All rights reserved.
# Distributed under the terms of the BSD

EAPI="7"

DESCRIPTION="empty project"
HOMEPAGE="http://fydeos.com"

LICENSE="BSD-Google"
SLOT="0"
KEYWORDS="amd64"
IUSE=""

RDEPEND="chromeos-base/vboot_reference"

DEPEND="${RDEPEND}"

S=${FILESDIR}

src_install() {
  exeinto /usr/sbin
  doexe crossystem_mode-switch.sh
}
