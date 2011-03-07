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