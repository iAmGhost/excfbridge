<div id='post'>
  <form action='/post/{{bid}}' method='post' onsubmit='return validate();'>
    <input type='text' id='post_subject' name='subject' maxlength='200' /><br />
    <textarea name='contents' id='post_contents' rows='8'></textarea>
    <input type='submit' value='게시' />
  </form>
</div>
