/**
 * MyFox portable launcher - launches Firefox with a portable profile.
 *
 * Compiled to MyFox.exe with Zig CC (~20 KB).
 *
 * Security note: This launcher executes whatever firefox.exe it finds at
 * App\Firefox64\firefox.exe (or App\Firefox\firefox.exe). It does NOT verify
 * the binary's Authenticode signature or hash. Users should ensure the
 * portable installation directory is not on a shared/untrusted drive.
 */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <shlwapi.h>
#include <strsafe.h>

#pragma comment(lib, "shlwapi.lib")

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
                    LPWSTR lpCmdLine, int nCmdShow) {
    (void)hInstance; (void)hPrevInstance; (void)lpCmdLine; (void)nCmdShow;

    WCHAR base[MAX_PATH];
    WCHAR ff_exe[MAX_PATH + 64];
    WCHAR profile[MAX_PATH + 64];
    WCHAR data_dir[MAX_PATH + 64];
    WCHAR ff_dir[MAX_PATH + 64];
    WCHAR cmdline[MAX_PATH * 3];

    /* Get directory where this exe lives */
    DWORD len = GetModuleFileNameW(NULL, base, MAX_PATH);
    if (len == 0 || len >= MAX_PATH) {
        MessageBoxW(NULL, L"Failed to get executable path.",
                    L"MyFox - Error", MB_ICONERROR);
        return 1;
    }
    PathRemoveFileSpecW(base);

    /* Try Firefox64 first, then Firefox */
    StringCchPrintfW(ff_exe, ARRAYSIZE(ff_exe),
                     L"%s\\App\\Firefox64\\firefox.exe", base);
    if (GetFileAttributesW(ff_exe) == INVALID_FILE_ATTRIBUTES) {
        StringCchPrintfW(ff_exe, ARRAYSIZE(ff_exe),
                         L"%s\\App\\Firefox\\firefox.exe", base);
        if (GetFileAttributesW(ff_exe) == INVALID_FILE_ATTRIBUTES) {
            MessageBoxW(NULL,
                L"Firefox not found.\n\n"
                L"Expected at:\n  App\\Firefox64\\firefox.exe\n  App\\Firefox\\firefox.exe",
                L"MyFox - Error", MB_ICONERROR);
            return 1;
        }
    }

    /* Ensure profile directory exists (parent first) */
    StringCchPrintfW(data_dir, ARRAYSIZE(data_dir), L"%s\\Data", base);
    StringCchPrintfW(profile, ARRAYSIZE(profile), L"%s\\Data\\profile", base);
    CreateDirectoryW(data_dir, NULL);
    CreateDirectoryW(profile, NULL);

    /* Build command line */
    StringCchPrintfW(cmdline, ARRAYSIZE(cmdline),
                     L"\"%s\" -profile \"%s\" -no-remote", ff_exe, profile);

    /* Get Firefox directory for working directory */
    StringCchCopyW(ff_dir, ARRAYSIZE(ff_dir), ff_exe);
    PathRemoveFileSpecW(ff_dir);

    /* Launch Firefox */
    STARTUPINFOW si = { .cb = sizeof(si) };
    PROCESS_INFORMATION pi = {0};

    if (!CreateProcessW(ff_exe, cmdline, NULL, NULL, FALSE,
                        DETACHED_PROCESS, NULL, ff_dir, &si, &pi)) {
        WCHAR err_msg[256];
        StringCchPrintfW(err_msg, ARRAYSIZE(err_msg),
            L"Failed to launch Firefox.\n\nError code: %lu", GetLastError());
        MessageBoxW(NULL, err_msg, L"MyFox - Error", MB_ICONERROR);
        return 1;
    }

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return 0;
}
