Name:           oreonvr-shell
Version:        2026.10.05
Release:        1%{?dist}
Summary:        Oreon VR spatial shell with a headless Plasma desktop bridge
License:        GPL-3.0-only AND OFL-1.1 AND Bitstream-Vera
URL:            https://github.com/oreonhq/oreonvr-shell
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  systemd-rpm-macros
BuildRequires:  kernel-headers
BuildRequires:  libjpeg-turbo-utils
BuildRequires:  libdrm-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  plasma-wayland-protocols
BuildRequires:  glib2-devel
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  pipewire-devel

Requires:       /usr/bin/kwin_wayland
Requires:       /usr/bin/plasmashell
Requires:       /usr/bin/pipewire
Requires:       /usr/bin/dbus-run-session
Requires:       /usr/bin/flatpak
Requires:       /usr/bin/curl
Requires:       /usr/bin/pdftoppm
Requires:       /usr/bin/gio
Requires:       /usr/bin/tar
Requires:       /usr/bin/lsblk
Requires:       /usr/bin/runuser
Requires:       /usr/bin/rsync
Requires:       /usr/bin/python3
Recommends:     centrio-installer
Recommends:     python3-pyside6
Recommends:     xdg-utils

%description
Oreon VR is a spatial shell for Oreon 11. It drives the screen (or a headset)
directly and shows floating panels: its own apps (Office, Surf, Store, files,
terminal) and the Oreon KDE Plasma desktop, which runs headless in KWin and is
streamed into the shell. Apps opened from the VR app grid float as their own
panels.

The package does not take over the boot on its own: enable
oreonvr-shell.service (and set multi-user.target as default) to boot into it.

%prep
%autosetup

%build
%set_build_flags
%make_build -C shell NO_SDL=1

%install
%make_install -C shell NO_SDL=1 PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} \
  LIBEXECDIR=%{_libexecdir} UNITDIR=%{_unitdir} USERUNITDIR=%{_userunitdir}

%check
# headless self-test: boots the scene, runs a short script, quits
OREONVR_NO_PTY=1 ./shell/oreonvr-shell --headless 640x400 --script 'wait 3; quit'

%post
%systemd_post oreonvr-shell.service
%systemd_user_post oreonvr-chromium-warmup.service

%preun
%systemd_preun oreonvr-shell.service
%systemd_user_preun oreonvr-chromium-warmup.service

%postun
# no restart on upgrade: that would close the running VR session
%systemd_postun oreonvr-shell.service
%systemd_user_postun oreonvr-chromium-warmup.service

%files
%license LICENSE shell/res/fonts/LICENSE-Inter.txt shell/res/fonts/LICENSE-DejaVu.txt
%doc README.md setup.md
%{_bindir}/oreonvr-shell
%{_libexecdir}/oreonvr-centrio-run
%{_libexecdir}/oreonvr-chromium
%{_libexecdir}/oreonvr-desktop-bridge
%{_libexecdir}/oreonvr-kwin
%{_libexecdir}/oreonvr-pick-user
%{_datadir}/oreonvr/
%{_unitdir}/oreonvr-shell.service
%{_userunitdir}/oreonvr-kde.service
%{_userunitdir}/oreonvr-plasma.service
%{_userunitdir}/oreonvr-chromium-warmup.service
%dir %{_sysconfdir}/oreonvr
%config(noreplace) %{_sysconfdir}/oreonvr/shell.conf
%config(noreplace) %{_sysconfdir}/oreonvr/desktop.conf

%changelog
* Mon Oct 05 2026 sk1lld <sk1lld@sk1lld.xyz> - 2026.10.05-1
- First package: the Oreon VR shell for Oreon 11 (KDE Plasma desktop bridge on KWin)
