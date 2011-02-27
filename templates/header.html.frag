<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="Content-Script-Type" content="text/javascript" />
    <meta http-equiv="Content-Style-Type" content="text/css" />
    <meta name="viewport" content="initial-scale=1.0" />
    <title>ⓢ.excf.com | {{title}}</title>
    <style type="text/css">
      @import url('/static/style.css');
    </style>
    <script type="text/javascript" src="/static/common.js"></script>
  </head>
  <body>
<div id='header'>
  <h2>{{title}}</h2>
  {% if signed_on %}<a class='button' href='/signoff'>로그아웃 ({{user}})</a>{% endif %}
</div>
<div id='body'>
