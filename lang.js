const MESSAGES = {
  en: {
    price_range: "Wheat price today is between ₹{min} and ₹{max}."
  },
  hi: {
    price_range: "आज गेहूं का भाव ₹{min} से ₹{max} के बीच है।"
  }
};

function getMessage(lang, key, data) {
  if (!MESSAGES[lang]) {
    console.warn(`Language "${lang}" not found, using English`);
    lang = "en";
  }
  
  if (!MESSAGES[lang][key]) {
    console.warn(`Message key "${key}" not found`);
    return "";
  }
  
  let msg = MESSAGES[lang][key];
  for (let k in data) {
    msg = msg.replace(`{${k}}`, data[k]);
  }
  return msg;
}
