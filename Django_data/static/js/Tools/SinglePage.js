async function fetchSection(section, request=null) {
  let response;

  if (!request) {
    response = await fetch(section);
  }
  else {
    response = await fetch(section, request);
  }

  if (!response.ok) {
    const _status = response.status;
    if (_status == 498 || _status == 499)
      throw new Error(_status + ':' + await response.text());
    else
      throw new Error(await response.text());
  }
  return response;
}

async function changeSection(section, content) {
  //tempDiv.innerHTML = await fetchSection(section);
  try {
    let	tempDiv = document.createElement('div');
    let response =  await MakeRequest(section);
    tempDiv.innerHTML = await response.text();

    let fetchedContent = await tempDiv.querySelector(content);
    document.querySelector(content).innerHTML = await fetchedContent.innerHTML;
  }
  catch (error) {
    throw new Error('ChangeSection Error: ', error);
  }
}

window.addEventListener('popstate', async function(event) {
  header_DelEvents();
  if (event.state == null) {
    await changeSection(`${ROUTE.HOME}`, '#content');
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    currentUrl = `${ROUTE.HOME}`;
  }
  else {
    await changeSection(event.state.section, '#content');
    await changeSection(`${ROUTE.HEADER}`, '#Header_content'); //add sonme handler event here
    currentUrl = event.state.section;
  }
  header_SetEvents();
});

async function loadPage(url) {
  if (typeof(url) != 'string' || !url || url === currentUrl) {
    return ;
  }
  currentUrl = url;
  history.pushState({section: url}, '', url);
  await changeSection(url, '#content');
}

async function	MakeRequest(url, request=null) {
  try {
    let response = await fetchSection(url, request);
    return response;
  }
  catch (err) {
    message = err.message;
    _words = message.split(':');
    if (_words[0] === '498') {
      console.log(`status => ${_words[0]}, reason => ${_words[1]}`);
      switch (_words[1]) {
	case 'Bad Issuer':
	  //Maybe del actual events
	  console.log('Bad Issuer token');
	  await put_signinPage();
	  throw new Error('JWT - 1');
	case 'Expired':
	  console.log('Expired token');
	  await fetchSection(`${ROUTE.JWTREFRESH}`);
	  response = await MakeRequest(url, request);
	  return response;
	case 'Bad Token':
	  console.log('Bad token');
	  await put_signinPage();
	  throw new Error('JWT - 2');
	default:
	  throw new Error('Error Encountered : ', await response.text());
      }
    }
    else if (_words[0] == '499') {
      console.log('Unauthorized token');
      await put_signinPage();
      throw new Error('JWT - 3');
    }
    else {
      throw new Error('Error Encountered : ', await response.text());
    }
  }
}

async function put_signinPage() {
  await loadPage(`${ROUTE.SIGNIN}`);
  header_DelEvents();
  await changeSection(`${ROUTE.HEADER}`, '#Header_content');
  header_SetEvents();
}
