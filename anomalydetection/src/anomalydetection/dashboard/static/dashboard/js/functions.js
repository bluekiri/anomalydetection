/**
 * Deserialize a query string.
 * @param serializedString
 * @return object
 */
function deserialize(serializedString){
  let str = decodeURI(serializedString);
  let pairs = str.split('&');
  let obj = {}, p, idx;
  let i = 0, n = pairs.length;
  for (; i < n; i++) {
    p = pairs[i].split('=');
    idx = p[0];

    if (idx.indexOf("[]") === (idx.length - 2)) {
      let ind = idx.substring(0, idx.length - 2);
      if (obj[ind] === undefined) {
        obj[ind] = [];
      }
      obj[ind].push(p[1]);
    }
    else {
      obj[idx] = p[1];
    }
  }
  return obj;
}
