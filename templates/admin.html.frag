<h2>열린 세션 (최근 {{limit_registry}}건)</h2>
<ul>
{% for ac in sessions %}<li>{{ac.signon_time}}: <b>{{ac.userid}}</b> ({{ac.phpsessid}})</li>{% endfor %}
</ul>
<h2>로그인 내역 (최근 {{limit_audit}}건)</h2>
<ul>
{% for al in audit %}<li>{{al.time}}: <b>{{al.userid}}</b> (from {{al.ipaddress}}{% if al.useragent %}, using {{al.useragent}}{% endif %})</li>{% endfor %}
</ul>
