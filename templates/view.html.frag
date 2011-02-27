<table id='view_header'>
  <tr>
    <th>이름</th>
    <td><span class='name'>{{name}}</span> <span class='id'>({{userid}})</span></td>
  </tr>
  <tr>
    <th>시각</th>
    <td>{{date}}</td>
  </tr>
{% if homepage %}
  <tr>
    <th>웹</th>
    <td><a href='{{homepage}}' target='_blank'>{{homepage}}</a></td>
  </tr>
{% endif %}
  <tr>
    <th>제목</th>
    <td>{{subject}}</td>
  </tr>
</table>
<div id='view_body'>
{{body}}
</div>
<table id='comments'>
{% for comment in comments %}
  <tr class='header'>
    <td class='author'><span class='name'>{{comment.name}}</span> <span class='id'>({{comment.id}})</span></td>
    <td class='date'>{{comment.date}}</td>
  </tr>
  <tr class='body'>
    <td colspan='2' class='body'>{{comment.body}}</td>
  </tr>
{% endfor %}
</table>
<div id='postcomment'>
<script type='text/javascript'>
  function validate() {
    if (!document.getElementById('input_comment').value) {
      alert('내용을 입력해 주십시오.);
      return false;
    }
    return true;
  }
</script>
<form action='/post_comment/{{bid}}/{{pid}}' method='post' onsubmit='return validate();'>
  <input id='input_comment' name='comment' maxlength='150'></textarea>
  <input id='input_submit' type='submit' value='게시' />
</form>
</div>
