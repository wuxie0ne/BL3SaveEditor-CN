using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Windows;
using System.Windows.Data;
using BL3Tools.GameData.Items;
using Newtonsoft.Json;

namespace BL3SaveEditor.Localization {
    // Display-only translations. The values bound to editing controls remain the original identifiers.
    public static class GameNames {
        private const string ResourceName = "BL3SaveEditor.Localization.GameNames.json";
        private static readonly Dictionary<string, Dictionary<string, string>> Tables = LoadTables();
        private static readonly Lazy<Dictionary<string, string>> AssetNames =
            new Lazy<Dictionary<string, string>>(BuildAssetNames);

        private static Dictionary<string, Dictionary<string, string>> LoadTables() {
            using (Stream stream = Assembly.GetExecutingAssembly().GetManifestResourceStream(ResourceName))
            using (var reader = new StreamReader(stream)) {
                return JsonConvert.DeserializeObject<Dictionary<string, Dictionary<string, string>>>(reader.ReadToEnd());
            }
        }

        public static string Translate(string category, string value) {
            if (value == null) return null;
            Dictionary<string, string> table;
            string translated;
            return Tables.TryGetValue(category, out table) && table.TryGetValue(value, out translated)
                ? translated : value;
        }

        private static Dictionary<string, string> BuildAssetNames() {
            var candidates = new Dictionary<string, HashSet<string>>(StringComparer.Ordinal);
            AddAssetNames(candidates, InventoryNameDatabase.NameDictionary, "names");
            AddAssetNames(candidates, InventoryNameDatabase.PrefixDictionary, "prefixes");
            return candidates.Where(x => x.Value.Count == 1)
                .ToDictionary(x => x.Key, x => x.Value.First(), StringComparer.Ordinal);
        }

        private static void AddAssetNames(Dictionary<string, HashSet<string>> candidates,
                Dictionary<string, string> source, string category) {
            foreach (var entry in source) {
                string translated = Translate(category, entry.Value);
                string shortName = entry.Key.Split('.').Last();
                HashSet<string> names;
                if (!candidates.TryGetValue(shortName, out names)) {
                    names = new HashSet<string>(StringComparer.Ordinal);
                    candidates.Add(shortName, names);
                }
                names.Add(translated);
            }
        }

        public static string Asset(string value) {
            if (value == null) return null;
            string translated;
            if (Tables["partEffects"].TryGetValue(value, out translated))
                return translated + " (" + value + ")";
            if (AssetNames.Value.TryGetValue(value, out translated) && translated != value)
                return translated + " (" + value + ")";

            // These are labels for identifier components, not descriptions of item effects.
            if (value.StartsWith("Part_", StringComparison.OrdinalIgnoreCase) ||
                value.StartsWith("GPart_", StringComparison.OrdinalIgnoreCase) ||
                value.IndexOf("_Part_", StringComparison.OrdinalIgnoreCase) >= 0 ||
                value.StartsWith("WeaponMayhemLevel_", StringComparison.OrdinalIgnoreCase)) {
                var partTypes = Tables["partTypes"];
                foreach (string token in value.Split('_')) {
                    if (partTypes.TryGetValue(token, out translated))
                        return translated + " (" + value + ")";
                }
            }
            return value;
        }

        public static string ItemName(Borderlands3Serial serial) {
            if (serial == null) return null;
            string original = serial.UserFriendlyName;
            string direct = Translate("names", original);
            if (direct != original) return direct;
            var parts = new List<string>(serial.Parts ?? new List<string>());
            if (serial.Balance != null) parts.Add(serial.Balance);
            string title = InventoryNameDatabase.GetNameForParts(parts, false);
            if (string.IsNullOrEmpty(title) || string.IsNullOrEmpty(original) || !original.EndsWith(title, StringComparison.Ordinal))
                return original;
            string prefix = original.Substring(0, original.Length - title.Length).TrimEnd();
            string translatedTitle = Translate("names", title);
            string translatedPrefix = Translate("prefixes", prefix);
            if (translatedTitle == title && translatedPrefix == prefix) return original;
            return string.IsNullOrEmpty(prefix) ? translatedTitle : translatedPrefix + " " + translatedTitle;
        }
    }

    public class GameNameConverter : IValueConverter {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture) {
            string text = value as string;
            if (text == null) return value;
            string category = parameter as string;
            return category == "asset" ? GameNames.Asset(text) : GameNames.Translate(category, text);
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture) {
            return DependencyProperty.UnsetValue;
        }
    }
}
