## Issue Title: Make efm-langserver command portable in Helix languages.toml

The current configuration in helix/languages.toml specifies the efm-langserver command as an absolute path:

    command = "/home/qlrd/go/bin/efm-langserver"

This makes the configuration less portable, since it is tied to your username and specific machine path. 

**Suggested improvements:**
- Use just "efm-langserver" if it is in the system $PATH.
- Consider using environment variables or document the path requirement.

**Example improvement:**

    command = "efm-langserver"

This change will make the config easier to share and use across machines.