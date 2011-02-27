<table id='list'>
  <thead>
    <tr>
      <th>제목</th>
      <th class='column_author'>글쓴이</th>
    </tr>
  </thead>
  <tbody>
{% for article in article_lists %}
    <tr>
      <td><a href='{{article.link}}'>{{article.name}} {% if article.comment %}<span class='comment'>{{article.comment}}</span>{% endif %}</a></td>
      <td class='column_author'>{{article.author}}</td>
    </tr>
{% endfor %}
  </tbody>
</table>
<table class='nav'>
  <tbody>
    <tr>
      <td><a href='/list/{{bid}}'>첫페이지로</a></td>
      <td><a href='/list/{{bid}}/{{page}}'>새로고침</a></td>
      <td><a href='/post/{{bid}}'>글쓰기</a></td>
  </tbody>
</table>
<div id='pagenav_container'>
  <table class='pagenav'>
    <tbody>
      <tr>
{% for p in pages %}
        <td class='pagebtn'><a href='/list/{{bid}}/{{p}}'>{{p}}</a></td>
{% endfor %}
      </tr>
    </tbody>
  </table>
</div>
      
