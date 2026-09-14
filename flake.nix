{
  # Minimal buildable flake so the trynix action ("nix in the browser") has a
  # real package to build, cache, and preview. This is intentionally small — a
  # reproducible static HTML index of the repo's skills — not a full app. The
  # dev environment lives in devenv (devenv.nix); this flake is only the build
  # target for CI previews.
  description = "ai-kitchen — buildable preview target for trynix (nix in the browser)";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      packages = forAllSystems (pkgs: {
        # `nix build .#default` — what the trynix workflow builds and previews.
        default = pkgs.runCommand "ai-kitchen-skills-index" { } ''
          mkdir -p "$out"
          {
            echo '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            echo '<meta name="viewport" content="width=device-width, initial-scale=1">'
            echo '<title>ai-kitchen skills</title>'
            echo '<style>body{font-family:-apple-system,system-ui,sans-serif;max-width:44rem;margin:3rem auto;padding:0 1rem;line-height:1.6;color:#1a1a1a}h1{font-size:1.6rem}code{background:#f0f0f0;padding:.1rem .35rem;border-radius:.25rem}li{margin:.3rem 0}footer{margin-top:2rem;color:#666;font-size:.85rem}</style>'
            echo '</head><body><h1>ai-kitchen — skills</h1><ul>'
            for d in ${self}/plugin/skills/*/; do
              [ -d "$d" ] || continue
              echo "<li><code>$(basename "$d")</code></li>"
            done
            echo '</ul><footer>Built reproducibly with Nix; previewed in-browser via trynix.</footer>'
            echo '</body></html>'
          } > "$out/index.html"
        '';
      });
    };
}
