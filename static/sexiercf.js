function sexiercf_contentreplacer(content) {
    filter = new Array();
    filterResult = new Array();
    
    filter.push(/^https?:\/\/.+?(\?v=|\/\d\/|\/embed\/|\/v\/|\.be\/)([a-zA-Z0-9\-\_]+)(\?.+)?$/gm);
    filterResult.push('<embed src="http://www.youtube.com/v/$2?version=3&amp;hl=ko_KR" type="application/x-shockwave-flash" width="560" height="315" allowscriptaccess="always" allowfullscreen="true"></embed>');
    
    filter.push(new RegExp('<iframe(.+?)</iframe>', "g"));
    filterResult.push('<embed$1</embed>');
    
    filter.push(new RegExp("<object.+?>(.*)</object>", "g"));
    filterResult.push('$1');
    
    filter.push(new RegExp("<param.+?>(.*)</param>", "g"));
    filterResult.push('');
    
    filter.push(new RegExp("<param.+?>", "g"));
    filterResult.push('');
    
    filter.push(new RegExp("^#(http(|s)://.+?)$", "gm"));
    filterResult.push('<img src="$1"/>');
    
    for (var i = 0; i < filter.length; i++) {
        content = content.replace(filter[i], filterResult[i]);
    }

    return content;
}