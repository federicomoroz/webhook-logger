DOCS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WEBHOOK LOGGER // FEDERICO MOROZ</title>
  <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
  <link rel="stylesheet" href="/static/terminal.css">
</head>
<body>
  <div id="docs-topbar">
    <a href="/" id="back-btn">&#8592; HOME</a>
    <span id="docs-title">WEBHOOK LOGGER &nbsp;//&nbsp; FEDERICO MOROZ &nbsp;//&nbsp; v1.0</span>
  </div>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {
      SwaggerUIBundle({
        url: "/openapi.json",
        dom_id: "#swagger-ui",
        deepLinking: true,
        presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
        layout: "BaseLayout",
        defaultModelsExpandDepth: -1,
      });
    };
  </script>
</body>
</html>"""
