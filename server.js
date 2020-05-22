var fs = require("fs"),
  exec = require("child_process").exec,
  fetch = require("node-fetch");
var csldat, slcdat;
var updCDat = async () => {
  //every hour update countries.json
  //var data=await (await fetch("https://api.covid19api.com/countries")).json();
  var data = (await (await fetch("https://api.covid19api.com/summary")).json())[
    "Countries"
  ];
  csldat = JSON.stringify(
    Object.fromEntries(data.map(e => [e["Country"], e["Slug"]]))
  );
  fs.writeFileSync("countriesSlug.json", csldat);
};
setInterval(updCDat, 3600000);
updCDat().then(() => {
  require("http")
    .createServer((req, res) => {
      var mimeType = "image/png";
      if (req.url.endsWith(".css")) {
        mimeType = "text/css";
      } else if (["", "/"].includes(req.url) || req.url.endsWith(".html")) {
        mimeType = "text/html";
      }
      res.writeHead(200, { "Content-Type": mimeType });
      if (["", "/"].includes(req.url)) {
        res.write(
          fs
            .readFileSync("public/index.html", "utf8")
            .replace(
              "***countries***",
              fs.readFileSync("countriesSlug.json", "utf8")
            )
        );
      } else if (req.url.startsWith("/c/")) {
        if (!fs.existsSync("/tmp/c")) fs.mkdirSync("/tmp/c");
        var execProcess = exec(
          'python3 server.py "' +
            req.url
              .substr(3)
              .toLowerCase()
              .replace(/%20/g, " ")
              .replace(/\"/g, "") +
            '"'
        );
        execProcess.stdout.pipe(process.stdout);
        execProcess.stderr.pipe(process.stderr);
        execProcess.on("exit", function() {
          var img =
            "/tmp" + req.url.toLowerCase().replace(/%20/g, " ") + ".png";
          if (fs.existsSync(img)) res.write(fs.readFileSync(img));
          res.end();
        });
        return;
      } else {
        if (fs.existsSync("public" + req.url))
          res.write(fs.readFileSync("public" + req.url, "utf8"));
      }
      res.end();
    })
    .listen(8080);
});
