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
  ['next' ,['proximo pergunta', 'proxima pergunta','proximo etapa', 'proxima etapa', 'proximo', 'proxima']]
];

var grammar_dict = {
  'yesno' : grammar_yesno,
  'pain_scale' : grammar_pain_scale,
  'general' : grammar_general
};

// var expected_answer_group = ['yesno','number','general'];
var expected_answer_group = ['yesno','pain_scale','general'];
var ind_transcribe_text_answer = true;
var ind_supress_text_answer = false;
var ind_found_match = false;
var utterance_is_talking = false;

var recognition_result_count = 1;
var recognition_count = 1;
var ending_timestamp;

var ind_mobile_or_tablet = mobileAndTabletcheck();

showInfo('ind_mobile_or_tablet: ' + ind_mobile_or_tablet, false);

if (!('webkitSpeechRecognition' in window)) {
    showInfo('webkitSpeechRecognition not in window => upgrade', true);
} else {
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.lang = 'pt-BR';
  recognition.start();

  recognition.onstart = function() {
    showInfo('recognition ' + recognition_count + ' has started', false, event.timeStamp);
  };

  // recognition.onaudiostart = function(event) {
  //   showInfo('recognition audio started', false, event.timeStamp);
  // };

  // recognition.onaudioend = function(event) {
  //   showInfo('recognition audio ended', false, event.timeStamp);
  // };

  recognition.onspeechstart = function (event) {
    showInfo('recognition speech started', false, event.timeStamp);
    // showInfo('recognition thinking has started', false);
  };

  // recognition.onspeechend = function (event) {
  //   showInfo('recognition speech ended', false, event.timeStamp);
  // };

  recognition.onerror = function(event) {
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
      if(event.results[i].isFinal){
          result_transcript += event.results[i][0].transcript;
      }
    }

    showInfo('result ' + recognition_count + '/' + recognition_result_count + ' - ' +  result_transcript, false, event.timeStamp);
    recognition_result_count++;

    if ( result_transcript) {
      getAnswerMatches(result_transcript);
    }
    // showInfo('recognition thinking has ended', false);
  };
}


function restartRecognition() {
  if(!utterance_is_talking){
    recognition_count++;
    recognition_result_count = 1;
    recognition.start();
  }
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
  if(ind_transcribe_text_answer && !ind_supress_text_answer && !ind_found_match){
    answer_textarea(result_transcript);
  } else {
    showInfo('Can not write because -- ind_transcribe_text_answer: ' + ind_transcribe_text_answer 
      + ', ind_supress_text_answer: ' + ind_supress_text_answer + ', ind_found_match: ' + ind_found_match, false);
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

  // Somente para debug, precisa adicionar os componentes ao HTML

  // var debug_area = document.getElementById("debug_area")
  // // console.log('aaaaaaaaaaaaaaaa')
  // if(debug_area){
  //   // console.log('bbbbbbbbbbbbbbbbb')
  //   var info_div = document.createElement('div')
  //   var info_span = document.createElement('span')
  //   info_div.innerHTML = '[' + formated_timestamp + '] $ > ';
  //   info_span.innerHTML = info;
  //   if(ind_alert){ 
  //     info_span.style.color = 'red';
  //   }
  //   info_div.appendChild(info_span);

  //   debug_area.appendChild(info_div);
  //   // console.log('cccccccccccc')
  // }


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
      text_area_value = text_area_element.value;
      // showInfo('text_area_value: \'' + text_area_value + '\'', true);
      // if(text_area_value){
      //   text_area_value += ' ';
      //   showInfo('*text_area_value: \'' + text_area_value + '\'', true);
      // }
      text_area_value += result_transcript;
      // showInfo('**text_area_value: \'' + text_area_value + '\'', true);
      text_area_element.value = text_area_value;
      // showInfo('***text_area_element.value: \'' + text_area_element.value + '\'', true);
    } else {
      showInfo('Elements for text area not found on page ', true);
    }
}

function answer_yesno(given_answer) {
  showInfo("answer_yesno" + ', given_answer: ' + given_answer,false);
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
    
      goToNetxtPage();
    } else {
      showInfo('Elements for yes or no answer not found on page ', true);
    }
}

function answer_pain_scale(given_answer) {
  showInfo("answer_pain_scale" + ', given_answer: ' + given_answer,false);

	var option_element = document.getElementById("pain_option_" + given_answer);
  if(option_element !==null){
    option_element.checked = true;
    option_element.focus();
    
    goToNetxtPage();
  } else {
    showInfo('Elements for pain scale not found on page ', true);
  }
}

function answer_general(given_answer) {
  showInfo("answer_general" + ', given_answer: ' + given_answer, false);

  switch(given_answer){
  case 'next':
    showInfo('Next page request detected', false);
    goToNetxtPage();
    break;
  case 'help':
    showInfo('Help request detected', true);
  }
}

function goToNetxtPage(){
  var btn_next = document.getElementById("btn_next");
  if(btn_next !==null){
    btn_next.click();
  } else {
    showInfo('Elements for pain scale not found on page ', true);
  }
}

function setExpectedAnswers(expectedAnswers){
  expected_answer_group = expectedAnswers;
}

function setIndTranscribeTextAnswer(should_transcribe){
  ind_transcribe_text_answer = should_transcribe;
  configTextAreaAndButton();
}

function checkIndSupressTextAnswer(){

  if(ind_supress_text_answer){
    ind_supress_text_answer = false;
  } else{
    ind_supress_text_answer = true;
  }
  // ind_supress_text_answer = !ind_supress_text_answer;
  configTextAreaAndButton();
}

function configTextAreaAndButton(){
  var btn_microphone_icon = document.getElementById("btn_microphone_icon");
  var text_area_element = document.getElementById("id_subject");
  if(btn_microphone_icon){
    if(ind_supress_text_answer){
      text_area_element.disabled = false;
      btn_microphone_icon.className = "fas fa-microphone-alt";
    } else {
      text_area_element.disabled = true;
      btn_microphone_icon.className = "fas fa-microphone-alt-slash";
    }
  }
}

function speakText() {
  var question_text = document.getElementById("question_text").innerHTML;
  var question_label = document.getElementById("question_label").innerHTML;
  
  if(question_text){
    textToSpeech(question_text);
  }
  if(question_label){
    textToSpeech(question_label);
  }
}

function textToSpeech(text) {
  showInfo('Text to speak: ' + text, false);
  var msg = new SpeechSynthesisUtterance();
  msg.voiceURI = 'native';
  msg.volume = 1; // 0 to 1
  msg.rate = 1; // 0.1 to 10
  msg.pitch = 0; //0 to 2
  msg.text = text;
  msg.lang = 'pt-BR';
  speechSynthesis.speak(msg);

  msg.onstart = function(event) {
    showInfo('Text to speak: ' + text, false);
    utterance_is_talking = true;
    recognition.stop();
  }

  msg.onend = function(event) {
    showInfo('Finished speaking after ' + event.elapsedTime + ' milliseconds', false);
    utterance_is_talking = false;
    restartRecognition();
  }
}

function mobileAndTabletcheck() {
  var check = false;
  (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
  return check;
};