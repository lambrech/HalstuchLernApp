using Microsoft.JSInterop;

namespace HalstuchLernApp.Services;

public class UpdateService
{
    private readonly IJSRuntime _jsRuntime;

    public UpdateService(IJSRuntime jsRuntime)
    {
        _jsRuntime = jsRuntime;
    }

    public async Task RegisterForUpdateAvailableAsync(Func<Task> onUpdateAvailable)
    {
        var dotNetRef = DotNetObjectReference.Create(new UpdateCallback(onUpdateAvailable));
        await _jsRuntime.InvokeVoidAsync("registerForUpdateAvailableNotification", dotNetRef, "OnUpdateAvailable");
    }

    public async Task CheckForUpdatesAsync()
    {
        await _jsRuntime.InvokeVoidAsync("checkForServiceWorkerUpdate");
    }

    public async Task InstallUpdateAsync()
    {
        await _jsRuntime.InvokeVoidAsync("installServiceWorkerUpdate");
    }

    public async Task ReloadPageAsync(bool clearCache = false)
    {
        if (clearCache)
        {
            await _jsRuntime.InvokeVoidAsync("reloadPageWithoutCache");
        }
        else
        {
            await _jsRuntime.InvokeVoidAsync("reloadPage");
        }
    }

    public async Task ClearCacheAsync()
    {
        await _jsRuntime.InvokeVoidAsync("clearAllCaches");
    }

    public class UpdateCallback
    {
        private readonly Func<Task> _callback;

        public UpdateCallback(Func<Task> callback)
        {
            _callback = callback;
        }

        [JSInvokable]
        public async Task OnUpdateAvailable()
        {
            await _callback();
        }
    }
}
