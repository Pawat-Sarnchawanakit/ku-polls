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

export function load_yaml(code) {
    try {
      const doc = yaml.load(code);
      if(doc == null || doc.poll == null)
        return "Poll missing.";
      let to_submit = [];
      const san = document.createElement("a");
      let html = ""
      const questions = new Set();
      for(let i = 0;i < doc.poll.length;++i) {
        const question = doc.poll[i];
        if(typeof(question) != "object")
          return "Questions must be an object."
        const question_var = Object.keys(question)[0];
        if(questions.has(question_var)) {
          return "Duplicated question: " + question_var;
        }
        questions.add(question_var);
        const content = question[question_var]
        if(content.type == null)
          return "Question must have a type."
        if(content.text == null)
          return "Question must have a text."
        html += "<div style=\"background-color: #3B3B3B;padding: 10px;margin: 15px;margin-left: auto;margin-right:auto;border-radius: 5px;width: min(600px, 70%)\">"
        san.innerText = content.text;
        html += "<h2 style=\"color: #FFF; margin: 0;margin-bottom: 5px;\">" + san.innerHTML + "</h2>"
        switch(content.type) {
          case "LABEL":
            san.innerText = content.label;
            html += "<p style=\"color: #FFF\;font-size: 12pt\">" + san.innerHTML + "</p>"
            break;
          case "CHOICE":
            to_submit.push({
              type: content.type,
              name: question_var
            })
            html += "<div id=\"pi_" + quoteattr(question_var) + "\" style=\"display: flex;flex-direction: column\">"
            if(content.choices == null)
              return "Choice questions must have choices."
            if(content.choices.length < 1)
              return "Choice questions must have at least 1 choice."
            const esc_q_var = quoteattr(question_var);
            const choices = new Set();
            for(let j = 0;j < content.choices.length;++j) {
              const choice = content.choices[j];
              if(typeof(choice) != "object")
                return "Choice must be an object."
              const choice_var = Object.keys(choice)[0];
              if(choices.has(choice_var)) {
                return "Duplicated chouce in `" + question_var + "`: " + choice_var;
              }
              choices.add(choice_var);
              const choice_content = choice[choice_var]
              san.innerText = choice_content;
              html += "<div style=\"display: flex;flex-direction: row\"><input type=\"radio\" style=\"color: #FFF\" name=\"" + esc_q_var + "\" choice=\"" + quoteattr(choice_var) + "\"><p style=\"color: #FFF;font-size: 12pt;margin-left: 7px\">" + san.innerHTML + "</p></div>"
            }
            html += "</div>"
            break;
          case "SHORT":
            to_submit.push({
              type: content.type,
              name: question_var
            })
            html += "<input id=\"pi_" + quoteattr(question_var) + "\" style=\"color: #FFF\; background-color: #2B2B2B;border: none; border-radius: 5px;width: 80%;font-size: 12pt\"></input>"
            break;
        }
        html += "</div>"
      }
      return {
        ok: true,
        content: html,
        doc: doc,
        answers: to_submit
      }
    } catch (e) {
      return e.message;
    }
}