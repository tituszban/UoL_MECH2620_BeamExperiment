#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#MaxThreadsPerHotkey 2

CoordMode, Mouse, Window

j::
	Loop 500,
	{
		Click, 100, 330
		Sleep, 500
		Click, 1100, 500
		Sleep, 23000
		Click, 1100, 340
		Sleep, 500
	}
	
Escape::
ExitApp
Return