import * as yaml from 'js-yaml';

function quoteattr(s) {
    return ('' + s) /* Forces the conversion to string. */
        .replace(/&/g, '&amp;') /* This MUST be the 1st replacement. */
        .replace(/'/g, '&apos;') /* The 4 other predefined entities, required. */
        .replace(/"/g, '&quot;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        /*
        You may add other replacements here for HTML only 
        (but it's not necessary).
        Or for XML, only if the named entities are defined in its DTD.
        */ 
        .replace(/\r\n/g, '\n') /* Must be before the next replacement. */
        .replace(/[\r\n]/g, '\n');
        ;
}

export const AllowType = {
  CLIENT: 1,
  AUTH: 1 << 1
};

export const ResType = {
  CREATOR: 1,
  AUTH: 1 << 1
};

export function validate_yaml(code) {
  let doc;
  try {
    doc = yaml.load(code);
  } catch(e) {
    return {
      ok: false,
      message: e.message
    };
  }
  if(doc == null || doc.poll == null)
    return {
      ok: false,
      message: "Poll missing."
    };
  doc.name = doc.name || "Unnamed poll";
  doc.image = doc.image || "";
  doc.begin = doc.begin || new Date/1E3|0;
  {
    doc.allow = doc.allow || "CLIENT";
    if(typeof(doc.allow) == "string")
      doc.allow = [ doc.allow ];
    if(!(doc.allow instanceof Array))
      return {
        ok: false,
        message: "allow must be string or a list of string."
      };
    let allow_int = 0;
    let allow_any = false;
    for(const allow of doc.allow) {
      switch(allow) {
        case "*":
          allow_any = true;
          break;
        case "CLIENT":
          allow_int |= AllowType.CLIENT;
          break;
        case "AUTH":
          allow_int |= AllowType.AUTH;
          break;
      }
    }
    if(allow_any)
      allow_int = 0;
    doc.allow = allow_int;
  }
  {
    doc.res = doc.res || "*";
    if(typeof(doc.res) == "string")
      doc.res = [ doc.res ];
    if(!(doc.res instanceof Array))
      return {
        ok: false,
        message: "res must be string or a list of string."
      };
    let res_int = 0;
    let res_any = false;
    for(const res of doc.res) {
      switch(res) {
        case "*":
          res_any = true;
          break;
        case "CREATOR":
          res_int |= ResType.CREATOR;
          break;
        case "AUTH":
          res_int |= ResType.AUTH;
          break;
      }
    }
    if(res_any)
      res_int = 0;
    doc.res = res_int;
  }
  const questions = new Set();
  for(const question_obj of doc.poll) {
    if(typeof(question_obj) != "object")
      return {
        ok: false,
        message: "Questions must be an object."
      };
    const question_var = Object.keys(question_obj)[0];
    if(questions.has(question_var))
      return {
        ok: false,
        message: "Duplicated question: `" + question_var + "`"
      };
    questions.add(question_var);
    const question = question_obj[question_var];
    if(question.type == null)
      return {
        ok: false,
        message: "Question `" + question_var + "` must have a type."
      };
    question.text = question.text || "";
    switch(question.type) {
      case "LABEL":
        question.label = question.label || "";
        break;
      case "CHOICE": {
        question.required = question.required || false;
        if(question.choices == null)
          return {
            ok: false,
            message: "Question `" + question_var + "` must have choices."
          };
        if(question.choices.length < 1)
          return {
            ok: false,
            message: "Question `" + question_var + "` must have at least 1 choice."
          };
        const choices = new Set();
        for(const choice of question.choices) {
          if(typeof(choice) != "object")
            return {
              ok: false,
              message: "A choice in question `" + question_var + "` must be an object."
            };
          const choice_var = Object.keys(choice)[0];
          if(choices.has(choice_var))
            return {
              ok: false,
              message: "Duplicated choice in question `" + question_var + "` named `" + choice_var + "`"
            };
          choices.add(choice_var);
        }
        break;
      }
      case "SHORT":
        break;
      default:
        return {
          ok: false,
          message: "Unknown question type in question `" + question_var + "`"
        };
    }
  }
  return {
    ok: true,
    yaml: doc
  };
}

export function display_poll(element, yaml, centered=true) {
  for(const question_obj of yaml.poll) {
    const question_var = Object.keys(question_obj)[0];
    const question = question_obj[question_var];
    const question_block = document.createElement("div");
    question_block.setAttribute("style", "background-color: #3B3B3B;padding: 10px;margin: 15px;" + (centered ? "margin-left: auto;margin-right:auto;" : "") + "border-radius: 5px;width: 600px");
    question_block.setAttribute("id", "pi_" + question_var);
    const block_text = document.createElement("h2");
    block_text.setAttribute("style", "color: #FFF; margin: 0;margin-bottom: 5px;");
    block_text.innerText = question.text;
    question_block.appendChild(block_text);
    switch(question.type) {
      case "LABEL": {
        const label = document.createElement("p");
        label.setAttribute("style", "color: #FFF\;font-size: 12pt");
        label.innerText = question.label;
        question_block.appendChild(label);
        break;
      }
      case "CHOICE": {
        const choices_block = document.createElement("div");
        choices_block.setAttribute("style", "display: flex;flex-direction: column");
        for(const choice of question.choices) {
          const choice_var = Object.keys(choice)[0];
          const choice_element = document.createElement("div");
          choice_element.setAttribute("style", "display: flex;flex-direction: row");
          const choice_radio = document.createElement("input");
          choice_radio.setAttribute("type", "radio");
          choice_radio.setAttribute("name", question_var);
          choice_radio.setAttribute("choice", choice_var);
          choice_element.appendChild(choice_radio);
          const choice_text = document.createElement("p");
          choice_text.setAttribute("style", "color: #FFF;font-size: 12pt;margin-left: 7px");
          choice_text.innerText = choice[choice_var];
          choice_element.appendChild(choice_text);
          choices_block.appendChild(choice_element);
        }
        question_block.append(choices_block);
        break;
      }
      case "SHORT": {
        const short_input = document.createElement("input");
        short_input.setAttribute("style", "color: #FFF; background-color: #2B2B2B;border: none; border-radius: 5px;width: 80%;font-size: 12pt");
        question_block.appendChild(short_input);
        break;
      }
    }
    element.appendChild(question_block);
  }
}

function getQuestionBlock(element, question_var) {
  for(const child of element.children)
    if(child.getAttribute("id") == "pi_" + question_var)
      return child;
  return null;
}

export function get_poll_answers(element, yaml) {
  let res = {};
  for(const question_obj of yaml.poll) {
    const question_var = Object.keys(question_obj)[0];
    const question = question_obj[question_var];
    switch(question.type) {
      case "CHOICE": {
        const blk = getQuestionBlock(element, question_var);
        if(!blk)
          return {
            ok: false,
            message: "Failed to question block for `" + question_var + "`"
          };
        const choice = blk.querySelector("div > input:checked");
        if(!choice) {
          if(question.required)
            return {
              ok: false,
              message: "You need to answer the question `" + (question.text || question_var) + "`"
            };
          continue;
        }
        res[question_var] = choice.getAttribute("choice");
        break;
      }
      case "SHORT": {
        const blk = getQuestionBlock(element, question_var);
        if(!blk)
          return {
            ok: false,
            message: "Failed to question block for `" + question_var + "`"
          };
        const input = blk.querySelector("input");
        if(!input)
          return {
            ok: false,
            message: "Failed to input block for `" + question_var + "`"
          };
        res[question_var] = input.value;  
        break;
      }
    }
  }
  return {
    ok: true,
    answers: res
  };
}

// try {
//   const doc = yaml.load(code);
//   if(doc == null || doc.poll == null)
//     return "Poll missing.";
//   let to_submit = [];
//   const san = document.createElement("a");
//   let html = ""
//   const questions = new Set();
//   for(let i = 0;i < doc.poll.length;++i) {
//     const question = doc.poll[i];
//     if(typeof(question) != "object")
//       return "Questions must be an object."
//     const question_var = Object.keys(question)[0];
//     if(questions.has(question_var)) {
//       return "Duplicated question: " + question_var;
//     }
//     questions.add(question_var);
//     const content = question[question_var]
//     if(content.type == null)
//       return "Question must have a type."
//     if(content.text == null)
//       return "Question must have a text."
//     html += "<div style=\"background-color: #3B3B3B;padding: 10px;margin: 15px;margin-left: auto;margin-right:auto;border-radius: 5px;width: min(600px, 70%)\">"
//     san.innerText = content.text;
//     html += "<h2 style=\"color: #FFF; margin: 0;margin-bottom: 5px;\">" + san.innerHTML + "</h2>"
//     switch(content.type) {
//       case "LABEL":
//         san.innerText = content.label;
//         html += "<p style=\"color: #FFF\;font-size: 12pt\">" + san.innerHTML + "</p>"
//         break;
//       case "CHOICE":
//         to_submit.push({
//           type: content.type,
//           name: question_var
//         })
//         html += "<div id=\"pi_" + quoteattr(question_var) + "\" style=\"display: flex;flex-direction: column\">"
//         if(content.choices == null)
//           return "Choice questions must have choices."
//         if(content.choices.length < 1)
//           return "Choice questions must have at least 1 choice."
//         const esc_q_var = quoteattr(question_var);
//         const choices = new Set();
//         for(let j = 0;j < content.choices.length;++j) {
//           const choice = content.choices[j];
//           if(typeof(choice) != "object")
//             return "Choice must be an object."
//           const choice_var = Object.keys(choice)[0];
//           if(choices.has(choice_var)) {
//             return "Duplicated chouce in `" + question_var + "`: " + choice_var;
//           }
//           choices.add(choice_var);
//           const choice_content = choice[choice_var]
//           san.innerText = choice_content;
//           html += "<div style=\"display: flex;flex-direction: row\"><input type=\"radio\" style=\"color: #FFF\" name=\"" + esc_q_var + "\" choice=\"" + quoteattr(choice_var) + "\"><p style=\"color: #FFF;font-size: 12pt;margin-left: 7px\">" + san.innerHTML + "</p></div>"
//         }
//         html += "</div>"
//         break;
//       case "SHORT":
//         to_submit.push({
//           type: content.type,
//           name: question_var
//         })
//         html += "<input id=\"pi_" + quoteattr(question_var) + "\" style=\"color: #FFF\; background-color: #2B2B2B;border: none; border-radius: 5px;width: 80%;font-size: 12pt\"></input>"
//         break;
//     }
//     html += "</div>"
//   }
//   return {
//     ok: true,
//     content: html,
//     doc: doc,
//     answers: to_submit
//   }
// } catch (e) {
//   return e.message;
// }