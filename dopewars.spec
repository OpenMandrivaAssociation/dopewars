%define name    dopewars
%define version 1.5.12
%define release %mkrel 2

%define title       Dopewars
%define longtitle   Make a fortune dealing drugs on the streets of New York

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Make a fortune dealing drugs on the streets of New York
License:        GPL
Group:          Games/Strategy
URL:            http://dopewars.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/dopewars/%{name}-%{version}.tar.bz2
Source11:       %{name}-16.png
Source12:       %{name}-32.png
Source13:       %{name}-48.png
Patch1:         %{name}-1.5.10-config.patch.bz2
BuildRequires:  gtk+2-devel
BuildRequires:  ncurses-devel
BuildRequires:  SDL-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:  esound-devel
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
perl -p -i -e 's|DPDATADIR|\"%{_datadir}\"|' src/dopewars.c  

%build
%configure  --bindir=%{_gamesbindir} \
        --datadir=%{_gamesdatadir} \
        --localstatedir=/var/lib/games
%make

%install
rm -rf %{buildroot}
%{makeinstall_std}
install -d %{buildroot}{%{_gamesdatadir},%{_sysconfdir},%{_localstatedir}/games}
mv %{buildroot}%{_gamesdatadir}/{doc,gnome,locale,pixmaps} $RPM_BUILD_ROOT%{_datadir}/
install -m 644 doc/example-cfg  %{buildroot}%{_sysconfdir}/%{name}

%{find_lang} %{name}

# icons
install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png 
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png 
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

# menu entry
mkdir -p %{buildroot}%{_menudir}
cat >%{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
    command="%{_gamesbindir}/%{name}" \
    needs="X11" \
    icon="%{name}.png" \
    section="More Applications/Games/Strategy" \
    title="%{title}" \
    longtitle="%{longtitle}" \
    xdg="true"
EOF

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=%{title}
Comment=%{longtitle}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=StrategyGame
EOF

# create highscore file
install -d %{buildroot}%{_localstatedir}/games
touch %{buildroot}%{_localstatedir}/games/%{name}.sco

%clean
rm -rf %{buildroot}

%post
%{update_menus}

%postun
%{clean_menus}

%files -f %{name}.lang
%defattr(-,root,root)
# not very nice, but it makes things work
%doc %{_datadir}/doc/*/
%config(noreplace) %{_sysconfdir}/%{name}
%{_libdir}/%{name}
%attr(2755,root,games) %{_gamesbindir}/dopewars
%attr(0664,root,games) %{_localstatedir}/games/%{name}.sco
%{_mandir}/man6/*
%{_datadir}/gnome/apps/Games/%{name}.desktop
%{_datadir}/pixmaps/*
%{_gamesdatadir}/%{name}
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
