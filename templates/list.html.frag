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
