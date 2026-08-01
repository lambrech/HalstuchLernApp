using System.Diagnostics;
using System.Linq;
using System.Reflection;

namespace HalstuchLernApp;

public static class Extensions
{
    public static (string version, string buildConfig, string commitId, string additionalCommitInfo, string fullVersionText) GetVersionInformation()
    {
        return GetVersionInformation(Assembly.GetEntryAssembly());
    }

    public static (string version, string buildConfig, string commitId, string additionalCommitInfo, string fullVersionText) GetVersionInformation(Assembly? assembly)
    {
        var attributes = assembly?.GetCustomAttributes(typeof(AssemblyInformationalVersionAttribute), false);
        Debug.Assert(attributes != null, nameof(attributes) + " != null");
        var fullVersionText = attributes.Length == 0
            ? $"Error getting Informational Version ... {assembly?.GetName().Version}"
            : ((AssemblyInformationalVersionAttribute)attributes[0]).InformationalVersion;

        var versionParts = fullVersionText.Split('|').Select(x => x.Trim()).ToList();

        if (versionParts.Count < 3)
        {
            return (fullVersionText, $"Found only {versionParts.Count} parts.", fullVersionText, fullVersionText, fullVersionText);
        }

        var version = versionParts[0];
        var buildConfig = versionParts[1].Replace(@"configName:", string.Empty);

        var isDirty = versionParts[2].Contains(@"-dirty");
        var tmpCommitId = versionParts[2].Replace(@"git:", string.Empty);

        if (isDirty)
        {
            tmpCommitId = tmpCommitId.Replace(@"-dirty", string.Empty);
        }

        var commitId = tmpCommitId.Length >= 40
            ? tmpCommitId.Substring(tmpCommitId.Length - 40, 40)
            : tmpCommitId;
        var additionalCommitInfo = versionParts.Count > 3
            ? $"{(isDirty ? "CAUTION! UNOFFICIAL/DIRTY BUILD VERSION!!! " : string.Empty)}{versionParts[3]}"
            : (isDirty ? "CAUTION! UNOFFICIAL/DIRTY BUILD VERSION!!!" : string.Empty);

        return (version, buildConfig, commitId, additionalCommitInfo, fullVersionText);
    }
}
