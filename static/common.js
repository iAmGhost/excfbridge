var Cookies = {
  init: function () {
    var allCookies = document.cookie.split('; ');
      for (var i=0;i<allCookies.length;i++) {
        var cookiePair = allCookies[i].split('=');
      this[cookiePair[0]] = unescape(cookiePair[1]);
    }
  },
  create: function (name,value,days) {
    if (days) {
      var date = new Date();
      date.setTime(date.getTime()+(days*24*60*60*1000));
      var expires = "; expires="+date.toGMTString();
    }
    else var expires = "";
    document.cookie = name+"="+escape(value)+expires+"; path=/";
    this[name] = value;
  },
  erase: function (name) {
    this.create(name,'',-1);
    this[name] = undefined;
  }
};
Cookies.init();

function jump(url) {
	if (url)
		document.location = url;
}

function confirmDelete()
{
	return confirm('삭제하시겠습니까?');
}

function nodoubleclick(target) {
    target.style.display = 'none';
}