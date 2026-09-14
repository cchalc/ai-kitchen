{ pkgs, ... }: {
  # Pull pre-built store paths from the public `cchalc` cachix cache.
  # https://devenv.sh/binary-caches/
  #
  # NOTE: for the daemon to actually honor this substituter, the machine must
  # either add the current user to `trusted-users` OR add the cache to
  # `trusted-substituters` in /etc/nix/nix.conf (a one-time, root-level step),
  # OR run `cachix use cchalc`. Otherwise nix ignores it with a warning for
  # untrusted users. CI runners are trusted, so the trynix workflow pulls fine.
  cachix.pull = [ "cchalc" ];

  languages.python.enable = true;
  languages.python.package = pkgs.python311;
  languages.python.uv.enable = true;

  enterShell = ''
    export UV_PROJECT_ENVIRONMENT="$HOME/.virtualenvs/ai-kitchen"
    if [ ! -d "$UV_PROJECT_ENVIRONMENT" ]; then
      uv sync
    fi
  '';
}
