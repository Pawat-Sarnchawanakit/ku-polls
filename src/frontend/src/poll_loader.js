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
      if(doc.poll == null)
        return "Poll missing.";
      const san = document.createElement("a");
      let html = ""
      for(let i = 0;i < doc.poll.length;++i) {
        const question = doc.poll[i];
        if(typeof(question) != "object")
          return "Questions must be an object."
        const question_var = Object.keys(question)[0];
        const content = question[question_var]
        if(content.type == null)
          return "Question must have a type."
        if(content.text == null)
          return "Question must have a text."
        html += "<div style=\"background-color: #3B3B3B;padding: 10px;margin: 10px;border-radius: 5px\">"
        san.innerText = content.text;
        html += "<h2 style=\"color: #FFF; margin: 0;margin-bottom: 5px;\">" + san.innerHTML + "</h2>"
        switch(content.type) {
          case "CHOICE":
            html += "<div style=\"display: flex;flex-direction: column\">"
            if(content.choices == null)
              return "Choice questions must have choices."
            const esc_q_var = quoteattr(question_var);
            for(let j = 0;j < content.choices.length;++j) {
              const choice = content.choices[j];
              if(typeof(choice) != "object")
                return "Choice must be an object."
              const choice_var = Object.keys(choice)[0];
              const choice_content = choice[choice_var]
              san.innerText = choice_content;
              html += "<div style=\"display: flex;flex-direction: row\"><input type=\"radio\" style=\"color: #FFF\" name=\"" + esc_q_var + "\"><p style=\"color: #FFF\">" + san.innerHTML + "</p></div>"
            }
            html += "</div>"
            break;
          case "SHORT":
            html += "<input style=\"color: #FFF\; background-color: #2B2B2B;border: none; border-radius: 5px\"></input>"
            break;
        }
        html += "</div>"
        // if(question.type)
      }
      return {
        ok: true,
        content: html
      }
      // console.log(doc.poll)
    } catch (e) {
      return e.message;
    }
}