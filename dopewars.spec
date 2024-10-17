%define name    dopewars
%define version 1.5.12
%define release 12

%define title       Dopewars
%define longtitle   Make a fortune dealing drugs on the streets of New York

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Make a fortune dealing drugs on the streets of New York
License:        GPL
Group:          Games/Strategy
URL:            https://dopewars.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/dopewars/%{name}-%{version}.tar.bz2
Source11:       %{name}-16.png
Source12:       %{name}-32.png
Source13:       %{name}-48.png
Patch1:         %{name}-1.5.10-config.patch
Patch2:         dopewars-1.5.12-fix-format-errors.patch
BuildRequires:  gtk+2-devel
BuildRequires:  ncurses-devel
BuildRequires:  SDL-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:  esound-devel
BuildRequires:	desktop-file-utils
Buildrequires:	recode
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
Based on John E. Dell's old Drug Wars game, dopewars is a simulation of an    
imaginary drug market.  dopewars is an All-American game which features       
buying, selling, and trying to get past the cops!                              

The first thing you need to do is pay off your debt to the Loan Shark. After   
that, your goal is to make as much money as possible (and stay alive)! You     
have one month of game time to make your fortune.                              

dopewars supports multiple players via. TCP/IP. Chatting to and fighting
with other players (computer or human) is supported; check the command line
switches (via dopewars -h) for further information. 

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
%configure2_5x  --bindir=%{_gamesbindir} \
        --datadir=%{_gamesdatadir} \
        --localstatedir=/var/lib/games
make

%install
rm -rf %{buildroot}
%{makeinstall_std}
install -d %{buildroot}{%{_gamesdatadir},%{_sysconfdir},%{_localstatedir}/lib/games}
mv %{buildroot}%{_gamesdatadir}/{doc,gnome,locale,pixmaps} %{buildroot}%{_datadir}/
install -m 644 doc/example-cfg  %{buildroot}%{_sysconfdir}/%{name}

%{find_lang} %{name}

# icons
install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png 
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png 
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

# menu entry
mkdir -p %{buildroot}/usr/share/applications
mv %{buildroot}%{_datadir}/gnome/apps/Games/%{name}.desktop \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

perl -pi -e 's,%{name}-weed.png,%{name}-weed,g' %{buildroot}%{_datadir}/applications/*

recode ISO-8859-15..UTF-8 %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Game;StrategyGame" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# create highscore file
install -d %{buildroot}%{_localstatedir}/lib/games
touch %{buildroot}%{_localstatedir}/lib/games/%{name}.sco

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files -f %{name}.lang
%defattr(-,root,root)
# not very nice, but it makes things work
%doc %{_datadir}/doc/*/
%config(noreplace) %{_sysconfdir}/%{name}
%{_libdir}/%{name}
%attr(2755,root,games) %{_gamesbindir}/dopewars
%attr(0664,root,games) %{_localstatedir}/lib/games/%{name}.sco
%{_mandir}/man6/*
%{_datadir}/pixmaps/*
%{_gamesdatadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.12-10mdv2011.0
+ Revision: 617873
- the mass rebuild of 2010.0 packages

* Sun Sep 13 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.12-9mdv2010.0
+ Revision: 438703
- fix format errors

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Wed Sep 03 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.12-7mdv2009.0
+ Revision: 279983
- fix sound file location (fix #43026)

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 1.5.12-6mdv2009.0
+ Revision: 244476
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Tue Feb 12 2008 Thierry Vignaud <tv@mandriva.org> 1.5.12-4mdv2008.1
+ Revision: 166599
- fix description-line-too-long
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Sep 13 2007 Emmanuel Andry <eandry@mandriva.org> 1.5.12-4mdv2008.0
+ Revision: 85308
- bump release
- buildrequires recode
- uncompress patch
- use provided desktop file
- convert desktop file to UTF8
- remove icon extension in desktop file
- Import dopewars



* Tue Aug 01 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.12-2mdv2007.0
- xdg menu

* Thu Jan 05 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.12-1mdk
- New release 1.5.12

* Mon Dec 12 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.10-3mdk
- Fixes from Anssi Hannula (<anssi.hannula@gmail.com>): 
 - fix BuildRequires
 - fix menudir
 - %%mkrel
- spec cleanup 

* Fri Dec 03 2004 David Walluck <walluck@mandrake.org> 1.5.10-2mdk
- fix local HTML doc link

* Wed Nov 10 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.5.10-1mdk
- 1.5.10
- drop P0, no need
- regenerate P1

* Thu Aug 26 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.5.9-5mdk
- rebuild for new menu
- don't bzip2 icons in src.rpm

* Fri Jul 09 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.5.9-4mdk 
- rpmbuilupdate aware
- fixed menu category
- fixed buildrequires syntax

* Sun Jul 27 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 1.5.9-3mdk
- fix configuration file problem
- fix high-score file problem
- fix executable perms

* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.5.9-2mdk
- rebuild
- change summary macro to avoid possible conflicts if we were to build debug package

* Wed Jun 11 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.5.9-1mdk
- 1.5.9

* Sat Jan 24 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.5.8-2mdk
- Create highscore file in install stage instead, no need for ghost file, and
  rpmlint gets happy:)
- Remove unneeded redundancy
- Don't rm -rf buildroot and install icons in prep stage, don't delete docs in
  install, (now possible to use --short-circuit)
- Quiet setup
- Make rpmlint more happy, longtitle, etc.
- Cleanups

* Sat Jan 04 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.5.8-1mdk
- 1.5.8

* Fri Aug 16 2002 Götz Waschk <waschk@linux-mandrake.com> 1.5.7-2mdk
- rebuild with new vorbis and gcc 3.2

* Wed Jun 26 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.5.7-1mdk
- 1.5.7
- menu entry
- config file
- better high score file handling
- more explicit summary :-)

* Fri Oct 26 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.5.2-2mdk
- new in contribs
- removed lurking cvs file

* Wed Oct 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.5.2-1mdk
- 1.5.2
- s/Copyright/License

* Tue May 15 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.5.0-1mdk
- first Mandrake release
