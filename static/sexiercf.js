function sexiercf_contentreplacer(content) {
    filter = new Array();
    filterResult = new Array();
    
    filter.push(/^http.+?(?:youtube\.com\/\S*(?:(?:\/e(?:mbed))?\/|watch\?(?:\S*?&?v\=))|youtu\.be\/)([a-zA-Z0-9_-]{6,11})/gm);
    filterResult.push('<embed src="http://www.youtube.com/v/$1?version=3&amp;hl=ko_KR" type="application/x-shockwave-flash" width="560" height="315" allowscriptaccess="always" allowfullscreen="true"></embed>\n유튜브 영상: <a href="https://youtu.be/$1">https://youtu.be/$1</a>');
    
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