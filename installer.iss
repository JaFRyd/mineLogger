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
var
  PortPage: TInputQueryWizardPage;

procedure InitializeWizard;
begin
  PortPage := CreateInputQueryPage(wpSelectDir,
    'Server Port',
    'Choose the port for the mineLogger web server.',
    'Enter a port number between 1024 and 65535. The default (5001) works for most setups.');
  PortPage.Add('Port:', False);
  PortPage.Values[0] := '5001';
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  Port: Integer;
begin
  Result := True;
  if CurPageID = PortPage.ID then
  begin
    Port := StrToIntDef(PortPage.Values[0], 0);
    if (Port < 1024) or (Port > 65535) then
    begin
      MsgBox('Please enter a valid port number between 1024 and 65535.', mbError, MB_OK);
      Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    SaveStringToFile(ExpandConstant('{app}\port.txt'), PortPage.Values[0], False);
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  // User data at %USERPROFILE%\.minelogger\ is intentionally preserved on uninstall
end;
