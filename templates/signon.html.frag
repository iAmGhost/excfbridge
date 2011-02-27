<script type='text/javascript'>
  function validate() {
    if (!document.getElementById('input_userid').value || !document.getElementById('input_password').value) {
      alert('아이디와 패스워드를 정확히 입력하여 주십시오.');
      return false;
    }

    nodoubleclick(document.getElementById('input_submit'));

    return true;
  }

  function nodoubleclick(target) {
    target.style.display = 'none';
  }
</script>
<form action='/signon' method='post' onsubmit='return validate();'>
  <table>
    <tbody>
      <tr>
	<th>아이디</th>
	<td><input id='input_userid' type='text' name='userid' size='15' value='{{userid}}' /></td>
      </tr>
      <tr>
	<th>패스워드</th>
	<td><input id='input_password' type='password' name='password' size='15' value='{{password}}' /></td>
      </tr>
      <tr>
	<th></th>
	<td><input id='input_saveform' type='checkbox' name='saveform' {{saveform}} /><label for='input_saveform'>로그인 정보 저장</label></td>
      </tr>
    </tbody>
  </table>
  <div class='disclaimer'>이 서비스는 여러분의 패스워드를 <span class='emph'>절대 결코 네버</span> 부정하게 취급하지 않으므로 걱정 붙들어 매셔도 좋습니다.</div>
  <div class='buttons'>
    <input type='button' onclick='history.back()' value='취소' />
    <input id='input_submit' type='submit' value='로그인' />
  </div>
</form>
