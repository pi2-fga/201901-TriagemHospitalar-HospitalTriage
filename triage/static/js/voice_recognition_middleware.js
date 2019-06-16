var has_error = false;
var grammar_yesno = 
[
  ['yes'  ,['sim', 'exatamente', 'isso mesmo']],
  ['no' ,['nao', 'negativo']]
];
var grammar_pain_scale = 
[
  // ['0'  ,['0','zero']],
  ['1'  ,['1','um']],
  ['2'  ,['2','dois']],
  ['3'  ,['3','tres']],
  ['4'  ,['4','quatro']],
  ['5'  ,['5','cinco']],
  ['6'  ,['6','seis']],
  ['7'  ,['7','sete']],
  ['8'  ,['8','oito']],
  ['9'  ,['9','nove']],
  ['10' ,['10','dez']]
];
var grammar_general = 
[
  ['help'  ,['ajuda', 'socorro', 'isso mesmo']],
  ['next' ,['proximo pergunta', 'proxima pergunta','proximo etapa', 'proxima etapa']]
];

var grammar_dict = {
  'yesno' : grammar_yesno,
  'pain_scale' : grammar_pain_scale,
  'general' : grammar_general
};

// var expected_answer_group = ['yesno','number','general'];
var expected_answer_group = ['yesno','pain_scale','general'];
var ind_transcribe_text_answer = true;
var ind_found_match = false;

var full_transcript = '';
var recognition_result_count = 1;
var recognition_count = 1;
var ending_timestamp;
if (!('webkitSpeechRecognition' in window)) {
    showInfo('webkitSpeechRecognition not in window => upgrade', true);
} else {
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.lang = 'pt-BR';
  recognition.start();

  recognition.onstart = function() {
    if( full_transcript){
      full_transcript += ' ';
    }
    showInfo('recognition ' + recognition_count + ' has started', false, event.timeStamp);
  };

  recognition.onaudiostart = function(event) {
    showInfo('recognition audio started', false, event.timeStamp);
  };

  recognition.onaudioend = function(event) {
    showInfo('recognition audio ended', false, event.timeStamp);
  };

  recognition.onspeechstart = function (event) {
    showInfo('recognition speech started', false, event.timeStamp);
    // showInfo('recognition thinking has started', false);
  };

  recognition.onspeechend = function (event) {
    showInfo('recognition speech ended', false, event.timeStamp);
  };

  recognition.onerror = function(event) {
    has_error = true;
    showInfo('recognition error - ' + event.error, true, event.timeStamp);
  };
  
  recognition.onnomatch = function(event) {
    showInfo('recognition no match', true, event.timeStamp);
  };

  recognition.onend = function() {
    var last_ending_timestamp = ending_timestamp;
    ending_timestamp = event.timeStamp;
    if (last_ending_timestamp !== undefined && ending_timestamp - last_ending_timestamp < 1000){
      showInfo('recognition ' + recognition_count + ' has ended to fast', true, event.timeStamp);
      setTimeout(function () {
        restartRecognition();
      }, 5000);

    } else {
      showInfo('recognition ' + recognition_count + ' has ended', false, event.timeStamp);
      restartRecognition();
    }
  };

  recognition.onresult = function(event) {
    var  result_transcript = '';
    for (var i = event.resultIndex; i < event.results.length; ++i) {
        result_transcript += event.results[i][0].transcript;
    }

    full_transcript +=  result_transcript;

    //// Somente para debug, precisa adicionar os componentes ao HTML
    // speech_text.innerHTML = full_transcript;

    showInfo('result ' + recognition_count + '/' + recognition_result_count + ' - ' +  result_transcript, false, event.timeStamp);
    recognition_result_count++;

    if ( result_transcript) {
      getAnswerMatches(result_transcript);
    }
    // showInfo('recognition thinking has ended', false);
  };
}


function restartRecognition() {
  recognition_count++;
  recognition_result_count = 1;
  recognition.start();
}

function getAnswerMatches(result_transcript){
  var grammar = '';
  for(var i = 0; i < expected_answer_group.length; i++) {
    var answer_group = expected_answer_group[i];
    grammar = grammar_dict[answer_group];
      
    // console.log('answer_group: '+answer_group);
    
    if(grammar){
      matchTranscriptAnswer(result_transcript, answer_group, grammar);
    } else {
      showInfo('answer type \'' + answer_group + '\' not found on expected answer types collection', true);
    }
  }
  if(ind_transcribe_text_answer && !ind_found_match){
    answer_textarea(result_transcript);
  } else {
    showInfo('ind_transcribe_text_answer: ' + ind_transcribe_text_answer + ', ind_found_match:' + ind_found_match, false);
  }
  ind_found_match = false;
}

function matchTranscriptAnswer(result_transcript, answer_group, grammar){
  // console.log('grammar: ' + grammar);
  for (var i = 0; i < grammar.length; i++) {
    // console.log('expected: ' + grammar[i][0]);
    // console.log('possible: ' + grammar[i][1]);
    var ind_match = false;
    var answer_item = grammar[i][0];
    var raw_answer_item = grammar[i][1];

    for (var j = 0; j < raw_answer_item.length; j++) {
      ind_match = result_transcript.normalize('NFD').replace(/[\u0300-\u036f]/g, "")
                                  .toLowerCase().includes(raw_answer_item[j]);
      // console.log('match_item: ' + raw_answer_item[j] + ' - ' + ind_match);
      if(ind_match){
        ind_found_match = true;
        registerMatch(answer_group, answer_item, raw_answer_item[j])
        break;
      }
    }
    // console.log(answer_group + ': ' + ind_match);
  }
}

function registerMatch(answer_group, answer_item, raw_answer_item){
    // console.log(answer_group + ': ' + answer_item + ': ' + raw_answer_item);

  var fun_answer = "answer_" + answer_group;
  this[fun_answer](answer_item);
  var match_info = 'result ' + recognition_count + '/' + recognition_result_count 
      + ' answer - ' + answer_group + ': ' + answer_item + ' (' + raw_answer_item + ')'

  //// Somente para debug, precisa adicionar os componentes ao HTML
  // var match_info_div = document.createElement('div')
  // match_info_div.innerHTML = match_info;
  // speech_match.appendChild(match_info_div);

  showInfo(match_info, false);
}

function showInfo(info, ind_alert, timestamp){
  var formated_timestamp = '';
  if (timestamp === undefined){ 
    formated_timestamp = '##:##:##';
  } else {
    formated_timestamp = formatTimestamp(timestamp);
  }

  //// Somente para debug, precisa adicionar os componentes ao HTML
  // var info_div = document.createElement('div')
  // var info_span = document.createElement('span')
  // info_div.innerHTML = '[' + formated_timestamp + '] $ > ';
  // info_span.innerHTML = info;
  // if(ind_alert){ 
  //   info_span.style.color = 'red';
  // }

  // info_div.appendChild(info_span);
  // speech_info.appendChild(info_div);


  if(ind_alert){ 
    console.log('%c' + info, "color: red");
  } else {
    console.log(info);
  }
}
function formatTimestamp(t){

  var date = new Date(t);

  var hour = date.getHours();
  var min = date.getMinutes();
  var sec = date.getSeconds();

  hour = (hour < 10 ? "0" : "") + hour;
  min = (min < 10 ? "0" : "") + min;
  sec = (sec < 10 ? "0" : "") + sec;

  var str =  hour + ":" + min + ":" + sec;
  return str;
}

function answer_textarea(result_transcript){
  var text_area_value = '';
  var text_area_element = document.getElementById("id_subject");
    if(text_area_element !==null){
      text_area_value = text_area_element.innerHTML;
      if(text_area_value){
        text_area_value += ' ';
      }
      text_area_value += result_transcript;
      text_area_element.innerHTML = text_area_value;
    } else {
      showInfo('Elements for text area not found on page ', true);
    }
}

function answer_yesno(given_answer) {
  console.log("answer_yesno" + ', given_answer: ' + given_answer);
  var option_element
  if (given_answer === 'yes') {
    option_element = document.querySelector("#id_boolean input[value='Sim']")
    // option_element = document.querySelector("input[type='radio']input[value='Sim']")
  } else if (given_answer === 'no'){
    option_element = document.querySelector("#id_boolean input[value='Não']")
    // option_element = document.querySelector("input[type='radio']input[value='Não']")
  }
    if(option_element !==null){
      option_element.checked = true;
    } else {
      showInfo('Elements for yes or no answer not found on page ', true);
    }
}

function answer_pain_scale(given_answer) {
  console.log("answer_pain_scale" + ', given_answer: ' + given_answer);

	var option_element = document.getElementById("pain_option_" + given_answer);
  if(option_element !==null){
    option_element.checked = true;
    option_element.focus();
  } else {
    showInfo('Elements for pain scale not found on page ', true);
  }
}

function answer_general(given_answer) {
  console.log("answer_general" + ', given_answer: ' + given_answer);

  switch(given_answer){
  case 'next':
    showInfo('Next page request detected', false);
    
    var btn_next = document.getElementById("btn_next");
    if(btn_next !==null){
      btn_next.click();
    } else {
      showInfo('Elements for pain scale not found on page ', true);
    }
    break;
  case 'help':
    showInfo('Help request detected', true);
  }
}

function setExpectedAnswers(expectedAnswers){
  expected_answer_group = expectedAnswers;
}

function setIndTranscribeTextAnswer(should_transcribe){
  ind_transcribe_text_answer = should_transcribe;
}