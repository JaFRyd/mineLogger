[Setup]
AppId={{A3F7B2C1-4D8E-4F9A-B6C2-1E3D5F7A9B0C}
AppName=mineLogger
AppVersion={#MyAppVersion}
AppPublisher=mineLogger
DefaultDirName={autopf}\mineLogger
DefaultGroupName=mineLogger
OutputDir=installer_output
OutputBaseFilename=minelogger-setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
UsedUserAreasWarning=no
DisableProgramGroupPage=yes
; User data (~/.minelogger/) is never touched by the installer or uninstaller

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "autostart"; Description: "Start mineLogger automatically at Windows login"; GroupDescription: "Additional options:"; Flags: checkedonce

[Files]
Source: "dist\minelogger\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "start-silent.vbs"; DestDir: "{app}"; Flags: ignoreversion
Source: "start-ui.vbs"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\mineLogger"; Filename: "wscript.exe"; Parameters: """{app}\start-ui.vbs"""; WorkingDir: "{app}"; Comment: "Open mineLogger web UI"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "mineLogger"; ValueData: "wscript.exe ""{app}\start-silent.vbs"""; Flags: uninsdeletevalue; Tasks: autostart

[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  // User data at %USERPROFILE%\.minelogger\ is intentionally preserved on uninstall
end;
