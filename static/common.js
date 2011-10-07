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

var cur_no = null;
var cur_name = null;
var cur_website = null;
var cur_email = null;

function setPopupLayer(no, name, website, email) 
{
	cur_no = no;
	cur_name = name;
	cur_website = website;
	cur_email = email;
	
	if (cur_website)
		document.getElementById('popup1').style.display = '';
	else
		document.getElementById('popup1').style.display = 'none';

	if (cur_email)
		document.getElementById('popup2').style.display = '';
	else
		document.getElementById('popup2').style.display = 'none';

	document.getElementById('popup_username').innerHTML = name;
	document.getElementById('popup').style.display = 'block';
	
	setTimeout(function() { document.onclick = checkClick; }, 0);
	// Workaround for iOS < 5
	if ((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i))) {
		window.onscroll = function() {
			document.getElementById('popup').style.top = window.pageYOffset + 'px';
		};
	}

	return false;
}

function hidePopupDiv()
{
	document.getElementById('popup').style.display = 'none';
}

function visitHome()
{
	hidePopupDiv();

	if (cur_website)
		document.location = cur_website;

	return false;
}

function sendMail()
{
	hidePopupDiv();

	if (cur_email)
		document.location = 'mailto:' + cur_email;

	return false;
}

function sendMessage()
{
	hidePopupDiv();
	
	if (cur_no)
		document.location = '/inbox/to/' + cur_no + '?qp=' + encodeURI(document.location.toString().replace('http://e.influx.kr', ''));

	return false;
}

function findByName()
{
	hidePopupDiv();
	
	if (cur_bid && cur_name)
		document.location = '/list/' + cur_bid + '/search/name_exact/' + cur_name;

	return false;
}

function checkClick(event)
{
	var elem = document.getElementById('popup');

	if (event.pageY >= window.pageYOffset + elem.offsetHeight) {
		hidePopupDiv();
		setTimeout(function() { document.onclick = null; }, 0);
		if ((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)))
			window.onscroll = null;
		return false;
	}

	return true;
}

function toggleStyle()
{
	if (Cookies['dark'])
		Cookies.erase('dark');
	else
		Cookies.create('dark', '1', 60 * 60 * 24 * 365);

	window.location.reload();

	return false;
}

