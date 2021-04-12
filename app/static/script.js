function createServerField() {
  var input = document.createElement('input');
  input.type = 'text';
  input.name = 'server[]';
  return input;
}

var form = document.getElementById('server_fields');
document.getElementById('addServer').addEventListener('click', function(e) {
  form.appendChild(createServerField());
});