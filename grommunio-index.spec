Name:		grommunio-index
Version:	1.7
Release:	1
Source0:	https://github.com/grommunio/grommunio-index/archive/refs/tags/%{version}.tar.gz#/grommunio-index-%{version}.tar.gz
Summary:	Full-text search index generator for grommunio-web
URL:		https://github.com/grommunio/grommunio-index
License:	AGPL-3.0
Group:		Servers
BuildSystem:	cmake
BuildRequires:	cmake(exmdbpp)
BuildRequires:	pkgconfig(libHX)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(mariadb)
BuildRequires:	pkgconfig(systemd)

Requires:	gromox
Requires:	grommunio-web

%description
grommunio-index builds and maintains SQLite FTS5 indexes used by
grommunio-web search. It is normally driven by the
grommunio-index.timer (every 15 minutes).

OpenMandriva stores indexes under /srv/grommunio/web/sqlite-index
(see /etc/gromox/index.cfg).

%prep -a
# Keep the stock /var/lib default in the binary; the OMV path is
# supplied via index.cfg so later local modifications stay easy.

%install -a
# Replace upstream sysusers (groweb group) with OMV identities
rm -f %{buildroot}%{_sysusersdir}/system-user-groindex.conf
cat >%{buildroot}%{_sysusersdir}/grommunio-index.conf <<'EOF'
u groindex - "grommunio fulltext indexer"
m groindex gromoxcf
m groindex www
m groindex grommunio
EOF

# Service runs as groindex:www so it can write the web index dir
sed -i \
	-e 's/^Group=.*/Group=www/' \
	-e 's/^SupplementaryGroups=.*/SupplementaryGroups=groindex gromoxcf grommunio/' \
	%{buildroot}%{_unitdir}/grommunio-index.service

install -d %{buildroot}%{_sysconfdir}/gromox
cat >%{buildroot}%{_sysconfdir}/gromox/index.cfg <<'EOF'
# OpenMandriva layout. See grommunio-index(8).
index_root = /srv/grommunio/web/sqlite-index
user = groindex
group = www
# -A also indexes public folders. Set to no to skip them.
# index_public = yes
EOF

%files
%{_bindir}/grommunio-index
%{_unitdir}/grommunio-index.service
%{_unitdir}/grommunio-index.timer
%{_sysusersdir}/grommunio-index.conf
%config(noreplace) %{_sysconfdir}/gromox/index.cfg
%doc %{_mandir}/man8/grommunio-index.8*
%license LICENSE.txt
