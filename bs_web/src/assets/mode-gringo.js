// {{{1 Lua Embedding

ace.define(
  "ace/mode/lua_highlight_rules",
  [
    "require",
    "exports",
    "module",
    "ace/lib/oop",
    "ace/mode/text_highlight_rules",
  ],
  function (require, exports, module) {
    "use strict";

    var oop = require("../lib/oop");
    var TextHighlightRules = require("./text_highlight_rules")
      .TextHighlightRules;

    var LuaHighlightRules = function () {
      var keywords =
        "break|do|else|elseif|end|for|function|if|in|local|repeat|" +
        "return|then|until|while|or|and|not";

      var builtinConstants = "true|false|nil|_G|_VERSION";

      var functions =
        "string|xpcall|package|tostring|print|os|unpack|require|" +
        "getfenv|setmetatable|next|assert|tonumber|io|rawequal|" +
        "collectgarbage|getmetatable|module|rawset|math|debug|" +
        "pcall|table|newproxy|type|coroutine|_G|select|gcinfo|" +
        "pairs|rawget|loadstring|ipairs|_VERSION|dofile|setfenv|" +
        "load|error|loadfile|" +
        "sub|upper|len|gfind|rep|find|match|char|dump|gmatch|" +
        "reverse|byte|format|gsub|lower|preload|loadlib|loaded|" +
        "loaders|cpath|config|path|seeall|exit|setlocale|date|" +
        "getenv|difftime|remove|time|clock|tmpname|rename|execute|" +
        "lines|write|close|flush|open|output|type|read|stderr|" +
        "stdin|input|stdout|popen|tmpfile|log|max|acos|huge|" +
        "ldexp|pi|cos|tanh|pow|deg|tan|cosh|sinh|random|randomseed|" +
        "frexp|ceil|floor|rad|abs|sqrt|modf|asin|min|mod|fmod|log10|" +
        "atan2|exp|sin|atan|getupvalue|debug|sethook|getmetatable|" +
        "gethook|setmetatable|setlocal|traceback|setfenv|getinfo|" +
        "setupvalue|getlocal|getregistry|getfenv|setn|insert|getn|" +
        "foreachi|maxn|foreach|concat|sort|remove|resume|yield|" +
        "status|wrap|create|running|" +
        "__add|__sub|__mod|__unm|__concat|__lt|__index|__call|__gc|__metatable|" +
        "__mul|__div|__pow|__len|__eq|__le|__newindex|__tostring|__mode|__tonumber";

      var stdLibaries = "string|package|os|io|math|debug|table|coroutine";

      var futureReserved = "";

      var deprecatedIn5152 = "setn|foreach|foreachi|gcinfo|log10|maxn";

      var keywordMapper = this.createKeywordMapper(
        {
          keyword: keywords,
          "support.function": functions,
          "invalid.deprecated": deprecatedIn5152,
          "constant.library": stdLibaries,
          "constant.language": builtinConstants,
          "invalid.illegal": futureReserved,
          "variable.language": "self",
        },
        "identifier"
      );

      var decimalInteger = "(?:(?:[1-9]\\d*)|(?:0))";
      var hexInteger = "(?:0[xX][\\dA-Fa-f]+)";
      var integer = "(?:" + decimalInteger + "|" + hexInteger + ")";

      var fraction = "(?:\\.\\d+)";
      var intPart = "(?:\\d+)";
      var pointFloat =
        "(?:(?:" + intPart + "?" + fraction + ")|(?:" + intPart + "\\.))";
      var floatNumber = "(?:" + pointFloat + ")";

      this.$rules = {
        start: [
          {
            stateName: "bracketedComment",
            onMatch: function (value, currentState, stack) {
              stack.unshift(this.next, value.length - 2, currentState);
              return "comment";
            },
            regex: /\-\-\[=*\[/,
            next: [
              {
                onMatch: function (value, currentState, stack) {
                  if (value.length == stack[1]) {
                    stack.shift();
                    stack.shift();
                    this.next = stack.shift();
                  } else {
                    this.next = "";
                  }
                  return "comment";
                },
                regex: /\]=*\]/,
                next: "start",
              },
              {
                defaultToken: "comment",
              },
            ],
          },

          {
            token: "comment",
            regex: "\\-\\-.*$",
          },
          {
            stateName: "bracketedString",
            onMatch: function (value, currentState, stack) {
              stack.unshift(this.next, value.length, currentState);
              return "comment";
            },
            regex: /\[=*\[/,
            next: [
              {
                onMatch: function (value, currentState, stack) {
                  if (value.length == stack[1]) {
                    stack.shift();
                    stack.shift();
                    this.next = stack.shift();
                  } else {
                    this.next = "";
                  }
                  return "comment";
                },

                regex: /\]=*\]/,
                next: "start",
              },
              {
                defaultToken: "comment",
              },
            ],
          },
          {
            token: "string", // " string
            regex: '"(?:[^\\\\]|\\\\.)*?"',
          },
          {
            token: "string", // ' string
            regex: "'(?:[^\\\\]|\\\\.)*?'",
          },
          {
            token: "constant.numeric", // float
            regex: floatNumber,
          },
          {
            token: "constant.numeric", // integer
            regex: integer + "\\b",
          },
          {
            token: keywordMapper,
            regex: "[a-zA-Z_$][a-zA-Z0-9_$]*\\b",
          },
          {
            token: "keyword.operator",
            regex:
              "\\+|\\-|\\*|\\/|%|\\#|\\^|~|<|>|<=|=>|==|~=|=|\\:|\\.\\.\\.|\\.\\.",
          },
          {
            token: "paren.lparen",
            regex: "[\\[\\(\\{]",
          },
          {
            token: "paren.rparen",
            regex: "[\\]\\)\\}]",
          },
          {
            token: "text",
            regex: "\\s+|\\w+",
          },
        ],
      };

      this.normalizeRules();
    };

    oop.inherits(LuaHighlightRules, TextHighlightRules);

    exports.LuaHighlightRules = LuaHighlightRules;
  }
);

ace.define(
  "ace/mode/python_highlight_rules",
  [
    "require",
    "exports",
    "module",
    "ace/lib/oop",
    "ace/mode/text_highlight_rules",
  ],
  function (require, exports, module) {
    "use strict";

    var oop = require("../lib/oop");
    var TextHighlightRules = require("./text_highlight_rules")
      .TextHighlightRules;

    var PythonHighlightRules = function() {

      var keywords = (
        "and|as|assert|break|class|continue|def|del|elif|else|except|exec|" +
        "finally|for|from|global|if|import|in|is|lambda|not|or|pass|print|" +
        "raise|return|try|while|with|yield|async|await|nonlocal"
      );

      var builtinConstants = (
        "True|False|None|NotImplemented|Ellipsis|__debug__"
      );

      var builtinFunctions = (
        "abs|divmod|input|open|staticmethod|all|enumerate|int|ord|str|any|" +
        "eval|isinstance|pow|sum|basestring|execfile|issubclass|print|super|" +
        "binfile|bin|iter|property|tuple|bool|filter|len|range|type|bytearray|" +
        "float|list|raw_input|unichr|callable|format|locals|reduce|unicode|" +
        "chr|frozenset|long|reload|vars|classmethod|getattr|map|repr|xrange|" +
        "cmp|globals|max|reversed|zip|compile|hasattr|memoryview|round|" +
        "__import__|complex|hash|min|apply|delattr|help|next|setattr|set|" +
        "buffer|dict|hex|object|slice|coerce|dir|id|oct|sorted|intern|" +
        "ascii|breakpoint|bytes"
      );
      var keywordMapper = this.createKeywordMapper({
        "invalid.deprecated": "debugger",
        "support.function": builtinFunctions,
        "variable.language": "self|cls",
        "constant.language": builtinConstants,
        "keyword": keywords
      }, "identifier");

      var strPre = "[uU]?";
      var strRawPre = "[rR]";
      var strFormatPre = "[fF]";
      var strRawFormatPre = "(?:[rR][fF]|[fF][rR])";
      var decimalInteger = "(?:(?:[1-9]\\d*)|(?:0))";
      var octInteger = "(?:0[oO]?[0-7]+)";
      var hexInteger = "(?:0[xX][\\dA-Fa-f]+)";
      var binInteger = "(?:0[bB][01]+)";
      var integer = "(?:" + decimalInteger + "|" + octInteger + "|" + hexInteger + "|" + binInteger + ")";

      var exponent = "(?:[eE][+-]?\\d+)";
      var fraction = "(?:\\.\\d+)";
      var intPart = "(?:\\d+)";
      var pointFloat = "(?:(?:" + intPart + "?" + fraction + ")|(?:" + intPart + "\\.))";
      var exponentFloat = "(?:(?:" + pointFloat + "|" + intPart + ")" + exponent + ")";
      var floatNumber = "(?:" + exponentFloat + "|" + pointFloat + ")";

      var stringEscape = "\\\\(x[0-9A-Fa-f]{2}|[0-7]{3}|[\\\\abfnrtv'\"]|U[0-9A-Fa-f]{8}|u[0-9A-Fa-f]{4})";

      this.$rules = {
        "start" : [ {
          token : "comment",
          regex : "#.*$"
        }, {
          token : "string",           // multi line """ string start
          regex : strPre + '"{3}',
          next : "qqstring3"
        }, {
          token : "string",           // " string
          regex : strPre + '"(?=.)',
          next : "qqstring"
        }, {
          token : "string",           // multi line ''' string start
          regex : strPre + "'{3}",
          next : "qstring3"
        }, {
          token : "string",           // ' string
          regex : strPre + "'(?=.)",
          next : "qstring"
        }, {
          token: "string",
          regex: strRawPre + '"{3}',
          next: "rawqqstring3"
        }, {
          token: "string",
          regex: strRawPre + '"(?=.)',
          next: "rawqqstring"
        }, {
          token: "string",
          regex: strRawPre + "'{3}",
          next: "rawqstring3"
        }, {
          token: "string",
          regex: strRawPre + "'(?=.)",
          next: "rawqstring"
        }, {
          token: "string",
          regex: strFormatPre + '"{3}',
          next: "fqqstring3"
        }, {
          token: "string",
          regex: strFormatPre + '"(?=.)',
          next: "fqqstring"
        }, {
          token: "string",
          regex: strFormatPre + "'{3}",
          next: "fqstring3"
        }, {
          token: "string",
          regex: strFormatPre + "'(?=.)",
          next: "fqstring"
        },{
          token: "string",
          regex: strRawFormatPre + '"{3}',
          next: "rfqqstring3"
        }, {
          token: "string",
          regex: strRawFormatPre + '"(?=.)',
          next: "rfqqstring"
        }, {
          token: "string",
          regex: strRawFormatPre + "'{3}",
          next: "rfqstring3"
        }, {
          token: "string",
          regex: strRawFormatPre + "'(?=.)",
          next: "rfqstring"
        }, {
          token: "keyword.operator",
          regex: "\\+|\\-|\\*|\\*\\*|\\/|\\/\\/|%|@|<<|>>|&|\\||\\^|~|<|>|<=|=>|==|!=|<>|="
        }, {
          token: "punctuation",
          regex: ",|:|;|\\->|\\+=|\\-=|\\*=|\\/=|\\/\\/=|%=|@=|&=|\\|=|^=|>>=|<<=|\\*\\*="
        }, {
          token: "paren.lparen",
          regex: "[\\[\\(\\{]"
        }, {
          token: "paren.rparen",
          regex: "[\\]\\)\\}]"
        }, {
          token: "text",
          regex: "\\s+"
        }, {
          include: "constants"
        }],
        "qqstring3": [{
          token: "constant.language.escape",
          regex: stringEscape
        }, {
          token: "string", // multi line """ string end
          regex: '"{3}',
          next: "start"
        }, {
          defaultToken: "string"
        }],
        "qstring3": [{
          token: "constant.language.escape",
          regex: stringEscape
        }, {
          token: "string",  // multi line ''' string end
          regex: "'{3}",
          next: "start"
        }, {
          defaultToken: "string"
        }],
        "qqstring": [{
          token: "constant.language.escape",
          regex: stringEscape
        }, {
          token: "string",
          regex: "\\\\$",
          next: "qqstring"
        }, {
          token: "string",
          regex: '"|$',
          next: "start"
        }, {
          defaultToken: "string"
        }],
        "qstring": [{
          token: "constant.language.escape",
          regex: stringEscape
        }, {
          token: "string",
          regex: "\\\\$",
          next: "qstring"
        }, {
          token: "string",
          regex: "'|$",
          next: "start"
        }, {
          defaultToken: "string"
        }],
        "rawqqstring3": [{
          token: "string", // multi line """ string end
          regex: '"{3}',
          next: "start"
        }, {
          defaultToken: "string"
        }],
        "rawqstring3": [{
          token: "string",  // multi line ''' string end
          regex: "'{3}",
          next: "start"
        }, {
          defaultToken: "string"
        }],
        "rawqqstring": [{
          token: "string",
          regex: "\\\\$",
          next: "rawqqstring"
        }, {
          token: "string",
          regex: '"|$',
          next: "start"
        }, {
          defaultToken: "string"
        }],
        "rawqstring": [{
          token: "string",
          regex: "\\\\$",
          next: "rawqstring"
        }, {
          token: "string",
          regex: "'|$",
          next: "start"
        }, {
          defaultToken: "string"
        }],
        "fqqstring3": [{
          token: "constant.language.escape",
          regex: stringEscape
        }, {
          token: "string", // multi line """ string end
          regex: '"{3}',
          next: "start"
        }, {
          token: "paren.lparen",
          regex: "{",
          push: "fqstringParRules"
        }, {
          defaultToken: "string"
        }],
        "fqstring3": [{
          token: "constant.language.escape",
          regex: stringEscape
        }, {
          token: "string",  // multi line ''' string end
          regex: "'{3}",
          next: "start"
        }, {
          token: "paren.lparen",
          regex: "{",
          push: "fqstringParRules"
        }, {
          defaultToken: "string"
        }],
        "fqqstring": [{
          token: "constant.language.escape",
          regex: stringEscape
        }, {
          token: "string",
          regex: "\\\\$",
          next: "fqqstring"
        }, {
          token: "string",
          regex: '"|$',
          next: "start"
        }, {
          token: "paren.lparen",
          regex: "{",
          push: "fqstringParRules"
        }, {
          defaultToken: "string"
        }],
        "fqstring": [{
          token: "constant.language.escape",
          regex: stringEscape
        }, {
          token: "string",
          regex: "'|$",
          next: "start"
        }, {
          token: "paren.lparen",
          regex: "{",
          push: "fqstringParRules"
        }, {
          defaultToken: "string"
        }],
        "rfqqstring3": [{
          token: "string", // multi line """ string end
          regex: '"{3}',
          next: "start"
        }, {
          token: "paren.lparen",
          regex: "{",
          push: "fqstringParRules"
        }, {
          defaultToken: "string"
        }],
        "rfqstring3": [{
          token: "string",  // multi line ''' string end
          regex: "'{3}",
          next: "start"
        }, {
          token: "paren.lparen",
          regex: "{",
          push: "fqstringParRules"
        }, {
          defaultToken: "string"
        }],
        "rfqqstring": [{
          token: "string",
          regex: "\\\\$",
          next: "rfqqstring"
        }, {
          token: "string",
          regex: '"|$',
          next: "start"
        }, {
          token: "paren.lparen",
          regex: "{",
          push: "fqstringParRules"
        }, {
          defaultToken: "string"
        }],
        "rfqstring": [{
          token: "string",
          regex: "'|$",
          next: "start"
        }, {
          token: "paren.lparen",
          regex: "{",
          push: "fqstringParRules"
        }, {
          defaultToken: "string"
        }],
        "fqstringParRules": [{//TODO: nested {}
          token: "paren.lparen",
          regex: "[\\[\\(]"
        }, {
          token: "paren.rparen",
          regex: "[\\]\\)]"
        }, {
          token: "string",
          regex: "\\s+"
        }, {
          token: "string",
          regex: "'(.)*'"
        }, {
          token: "string",
          regex: '"(.)*"'
        }, {
          token: "function.support",
          regex: "(!s|!r|!a)"
        }, {
          include: "constants"
        },{
          token: 'paren.rparen',
          regex: "}",
          next: 'pop'
        },{
          token: 'paren.lparen',
          regex: "{",
          push: "fqstringParRules"
        }],
        "constants": [{
          token: "constant.numeric", // imaginary
          regex: "(?:" + floatNumber + "|\\d+)[jJ]\\b"
        }, {
          token: "constant.numeric", // float
          regex: floatNumber
        }, {
          token: "constant.numeric", // long integer
          regex: integer + "[lL]\\b"
        }, {
          token: "constant.numeric", // integer
          regex: integer + "\\b"
        }, {
          token: ["punctuation", "function.support"],// method
          regex: "(\\.)([a-zA-Z_]+)\\b"
        }, {
          token: keywordMapper,
          regex: "[a-zA-Z_$][a-zA-Z0-9_$]*\\b"
        }]
      };
      this.normalizeRules();
    };

    oop.inherits(PythonHighlightRules, TextHighlightRules);

    exports.PythonHighlightRules = PythonHighlightRules;
  }
);


ace.define(
  "ace/mode/folding/lua",
  [
    "require",
    "exports",
    "module",
    "ace/lib/oop",
    "ace/mode/folding/fold_mode",
    "ace/range",
    "ace/token_iterator",
  ],
  function (require, exports, module) {
    "use strict";

    var oop = require("../../lib/oop");
    var BaseFoldMode = require("./fold_mode").FoldMode;
    var Range = require("../../range").Range;
    var TokenIterator = require("../../token_iterator").TokenIterator;

    var FoldMode = (exports.FoldMode = function () {});

    oop.inherits(FoldMode, BaseFoldMode);

    (function () {
      this.foldingStartMarker = /\b(function|then|do|repeat)\b|{\s*$|(\[=*\[)/;
      this.foldingStopMarker = /\bend\b|^\s*}|\]=*\]/;

      this.getFoldWidget = function (session, foldStyle, row) {
        var line = session.getLine(row);
        var isStart = this.foldingStartMarker.test(line);
        var isEnd = this.foldingStopMarker.test(line);

        if (isStart && !isEnd) {
          var match = line.match(this.foldingStartMarker);
          if (match[1] == "then" && /\belseif\b/.test(line)) return;
          if (match[1]) {
            if (session.getTokenAt(row, match.index + 1).type === "keyword")
              return "start";
          } else if (match[2]) {
            var type = session.bgTokenizer.getState(row) || "";
            if (type[0] == "bracketedComment" || type[0] == "bracketedString")
              return "start";
          } else {
            return "start";
          }
        }
        if (foldStyle != "markbeginend" || !isEnd || (isStart && isEnd))
          return "";

        var match = line.match(this.foldingStopMarker);
        if (match[0] === "end") {
          if (session.getTokenAt(row, match.index + 1).type === "keyword")
            return "end";
        } else if (match[0][0] === "]") {
          var type = session.bgTokenizer.getState(row - 1) || "";
          if (type[0] == "bracketedComment" || type[0] == "bracketedString")
            return "end";
        } else return "end";
      };

      this.getFoldWidgetRange = function (session, foldStyle, row) {
        var line = session.doc.getLine(row);
        var match = this.foldingStartMarker.exec(line);
        if (match) {
          if (match[1]) return this.luaBlock(session, row, match.index + 1);

          if (match[2])
            return session.getCommentFoldRange(row, match.index + 1);

          return this.openingBracketBlock(session, "{", row, match.index);
        }

        var match = this.foldingStopMarker.exec(line);
        if (match) {
          if (match[0] === "end") {
            if (session.getTokenAt(row, match.index + 1).type === "keyword")
              return this.luaBlock(session, row, match.index + 1);
          }

          if (match[0][0] === "]")
            return session.getCommentFoldRange(row, match.index + 1);

          return this.closingBracketBlock(
            session,
            "}",
            row,
            match.index + match[0].length
          );
        }
      };

      this.luaBlock = function (session, row, column) {
        var stream = new TokenIterator(session, row, column);
        var indentKeywords = {
          function: 1,
          do: 1,
          then: 1,
          elseif: -1,
          end: -1,
          repeat: 1,
          until: -1,
        };

        var token = stream.getCurrentToken();
        if (!token || token.type != "keyword") return;

        var val = token.value;
        var stack = [val];
        var dir = indentKeywords[val];

        if (!dir) return;

        var startColumn =
          dir === -1
            ? stream.getCurrentTokenColumn()
            : session.getLine(row).length;
        var startRow = row;

        stream.step = dir === -1 ? stream.stepBackward : stream.stepForward;
        while ((token = stream.step())) {
          if (token.type !== "keyword") continue;
          var level = dir * indentKeywords[token.value];

          if (level > 0) {
            stack.unshift(token.value);
          } else if (level <= 0) {
            stack.shift();
            if (!stack.length && token.value != "elseif") break;
            if (level === 0) stack.unshift(token.value);
          }
        }

        var row = stream.getCurrentTokenRow();
        if (dir === -1)
          return new Range(
            row,
            session.getLine(row).length,
            startRow,
            startColumn
          );
        else
          return new Range(
            startRow,
            startColumn,
            row,
            stream.getCurrentTokenColumn()
          );
      };
    }.call(FoldMode.prototype));
  }
);

ace.define(
  "ace/mode/lua",
  [
    "require",
    "exports",
    "module",
    "ace/lib/oop",
    "ace/mode/text",
    "ace/mode/lua_highlight_rules",
    "ace/mode/folding/lua",
    "ace/range",
    "ace/worker/worker_client",
  ],
  function (require, exports, module) {
    "use strict";

    var oop = require("../lib/oop");
    var TextMode = require("./text").Mode;
    var LuaHighlightRules = require("./lua_highlight_rules").LuaHighlightRules;
    var LuaFoldMode = require("./folding/lua").FoldMode;
    var Range = require("../range").Range;
    var WorkerClient = require("../worker/worker_client").WorkerClient;

    var Mode = function () {
      this.HighlightRules = LuaHighlightRules;

      this.foldingRules = new LuaFoldMode();
    };
    oop.inherits(Mode, TextMode);

    (function () {
      this.lineCommentStart = "--";
      this.blockComment = { start: "--[", end: "]--" };

      var indentKeywords = {
        function: 1,
        then: 1,
        do: 1,
        else: 1,
        elseif: 1,
        repeat: 1,
        end: -1,
        until: -1,
      };
      var outdentKeywords = ["else", "elseif", "end", "until"];

      function getNetIndentLevel(tokens) {
        var level = 0;
        for (var i = 0; i < tokens.length; i++) {
          var token = tokens[i];
          if (token.type == "keyword") {
            if (token.value in indentKeywords) {
              level += indentKeywords[token.value];
            }
          } else if (token.type == "paren.lparen") {
            level++;
          } else if (token.type == "paren.rparen") {
            level--;
          }
        }
        if (level < 0) {
          return -1;
        } else if (level > 0) {
          return 1;
        } else {
          return 0;
        }
      }

      this.getNextLineIndent = function (state, line, tab) {
        var indent = this.$getIndent(line);
        var level = 0;

        var tokenizedLine = this.getTokenizer().getLineTokens(line, state);
        var tokens = tokenizedLine.tokens;

        if (state == "start") {
          level = getNetIndentLevel(tokens);
        }
        if (level > 0) {
          return indent + tab;
        } else if (
          level < 0 &&
          indent.substr(indent.length - tab.length) == tab
        ) {
          if (!this.checkOutdent(state, line, "\n")) {
            return indent.substr(0, indent.length - tab.length);
          }
        }
        return indent;
      };

      this.checkOutdent = function (state, line, input) {
        if (input != "\n" && input != "\r" && input != "\r\n") return false;

        if (line.match(/^\s*[\)\}\]]$/)) return true;

        var tokens = this.getTokenizer().getLineTokens(line.trim(), state)
          .tokens;

        if (!tokens || !tokens.length) return false;

        return (
          tokens[0].type == "keyword" &&
          outdentKeywords.indexOf(tokens[0].value) != -1
        );
      };

      this.autoOutdent = function (state, session, row) {
        var prevLine = session.getLine(row - 1);
        var prevIndent = this.$getIndent(prevLine).length;
        var prevTokens = this.getTokenizer().getLineTokens(prevLine, "start")
          .tokens;
        var tabLength = session.getTabString().length;
        var expectedIndent =
          prevIndent + tabLength * getNetIndentLevel(prevTokens);
        var curIndent = this.$getIndent(session.getLine(row)).length;
        if (curIndent < expectedIndent) {
          return;
        }
        session.outdentRows(new Range(row, 0, row + 2, 0));
      };

      this.createWorker = function (session) {
        var worker = new WorkerClient(["ace"], "ace/mode/lua_worker", "Worker");
        worker.attachToDocument(session.getDocument());

        worker.on("annotate", function (e) {
          session.setAnnotations(e.data);
        });

        worker.on("terminate", function () {
          session.clearAnnotations();
        });

        return worker;
      };

      this.$id = "ace/mode/lua";
    }.call(Mode.prototype));

    exports.Mode = Mode;
  }
);

// {{{1 Gringo Highlighting

ace.define(
  "ace/mode/gringo_highlight_rules",
  [
    "require",
    "exports",
    "module",
    "ace/lib/oop",
    "ace/mode/text_highlight_rules",
  ],
  function (require, exports, module) {
    "use strict";

    var oop = require("../lib/oop");
    var TextHighlightRules = require("./text_highlight_rules")
      .TextHighlightRules;
    var LuaHighlightRules = ace.require("ace/mode/lua_highlight_rules")
      .LuaHighlightRules;
    var PythonHighlightRules = ace.require("ace/mode/python_highlight_rules")
      .PythonHighlightRules;

    var GringoHighlightRules = function () {
      this.$rules = {
        start: [
          { include: "#comment" },
          { include: "#lua" },
          { include: "#python" },
          { include: "#weak" },
          { include: "#statement" },
        ],
        "#lua": [
          {
            token: [
              "keyword.control",
              "punctuation.separator",
              "entity.name",
              "punctuation.separator",
            ],
            regex: "(#script)\\s*(\\()\\s*(lua)\\s*(\\))",
            next: "lua-start",
          },
        ],
        "#python": [
          {
            token: [
              "keyword.control",
              "punctuation.separator",
              "entity.name",
              "punctuation.separator",
            ],
            regex: "(#script)\\s*(\\()\\s*(python)\\s*(\\))",
            next: "python-start",
          },
        ],
        "#comment": [
          {
            // block comment
            token: "punctuation.definition.comment.gringo",
            regex: "%\\*",
            push: [
              {
                token: "punctuation.definition.comment.gringo",
                regex: "\\*%",
                next: "pop",
              },
              { include: "#comment" }, // allow for nesting
              { defaultToken: "comment.block.gringo" },
            ],
          },
          {
            // line comment
            token: [
              "punctuation.definition.comment.gringo",
              "comment.line.percentage.gringo",
            ],
            regex: "(%)(.*$)",
          },
        ],
        "#keyword": [
          {
            token: "keyword.control",
            regex:
              "#include\\b|#show\\b|#program\\b|#const\\b|#sum\\+|#sum\\b|#count\\b|#minimize\\b|#maximize\\b|#true\\b|#false\\b|#theory\\b",
          },
        ],
        "#operator": [
          {
            token: "keyword.operator.gringo",
            regex:
              "\\bnot\\b|[><]=?|[!]?=|\\.\\.|\\+|-|\\*|/|\\|\\?|\\^|~|@|&|\\|",
          },
        ],
        "#punctuation": [
          {
            token: "punctuation.separator",
            regex: ",|\\:-|\\:~|\\:|{|}|\\(|\\)|;",
          },
        ],
        "#identifier": [
          { token: "entity.name", regex: "\\b([_]*[a-z][a-zA-Z0-9_']*)" },
        ],
        "#number": [
          { token: "constant.numeric", regex: "\\b0|([1-9][0-9]*)\\b" },
        ],
        "#variable": [
          { token: "variable.other", regex: "\\b([_]*[A-Z][a-zA-Z0-9_']*)" },
          { token: "variable.language", regex: "\\b_\\b" },
        ],
        "#string": [
          {
            token: "string.quoted",
            regex: '"',
            push: [
              { token: "constant.character", regex: "\\\\\\\\" },
              { token: "constant.character", regex: '\\\\"' },
              { token: "string.quoted", regex: '"', next: "pop" },
              { defaultToken: "string.quoted" },
            ],
          },
        ],
        "#weak": [
          {
            token: "punctuation.separator",
            regex: "\\[",
            push: [
              { include: "#punctuation" },
              { include: "#operator" },
              { include: "#identifier" },
              { include: "#number" },
              { include: "#variable" },
              { include: "#string" },
              { token: "punctuation.separator", regex: "\\]", next: "pop" },
              { token: "invalid.illegal", regex: "[^\\s]" },
            ],
          },
        ],
        "#statement": [
          {
            token: "meta.statement.gringo",
            regex: "(?=[^\\s])",
            push: [
              { include: "#punctuation" },
              { include: "#operator" },
              { include: "#identifier" },
              { include: "#number" },
              { include: "#variable" },
              { include: "#keyword" },
              { include: "#string" },
              { token: "punctuation", regex: "\\.", next: "pop" },
              { token: "invalid.illegal", regex: "[^\\s]" },
            ],
          },
        ],
      };

      this.embedRules(LuaHighlightRules, "lua-", [
        {
          token: "keyword.control",
          regex: "#end\\s*\\.",
          next: "start",
        },
      ]);

      this.embedRules(PythonHighlightRules, "python-", [
        {
          token: "keyword.control",
          regex: "#end\\s*\\.",
          next: "start",
        },
      ]);

      this.normalizeRules();

      this.metaData = {
        fileTypes: ["gringo"],
        name: "Gringo",
        scopeName: "source.gringo",
      };
    };

    oop.inherits(GringoHighlightRules, TextHighlightRules);

    exports.GringoHighlightRules = GringoHighlightRules;
  }
);

// {{{1 Gringo Mode

ace.define(
  "ace/mode/gringo",
  [
    "require",
    "exports",
    "module",
    "ace/lib/oop",
    "ace/mode/text",
    "ace/mode/gringo_highlight_rules",
    "ace/mode/folding/cstyle",
  ],
  function (require, exports, module) {
    "use strict";

    var oop = require("../lib/oop");
    var TextMode = require("./text").Mode;
    var GringoHighlightRules = require("./gringo_highlight_rules")
      .GringoHighlightRules;

    var Mode = function () {
      var LuaMode = require("ace/mode/lua").Mode;
      this.HighlightRules = GringoHighlightRules;
      this.createModeDelegates({ "lua-": LuaMode });
    };
    oop.inherits(Mode, TextMode);

    (function () {
      this.lineCommentStart = "%";
      this.blockComment = { start: "%*", end: "*%" };
      this.$id = "ace/mode/gringo";
    }.call(Mode.prototype));

    exports.Mode = Mode;
  }
);