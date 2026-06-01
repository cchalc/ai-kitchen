{ pkgs, ... }: {
  # Disable cachix binary cache management — requires trusted-user in nix.conf.
  # Without this, devenv fails to evaluate when the user is not trusted.
  cachix.enable = false;

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
