/*
 Anomaly Detection Framework
 Copyright (C) 2018 Bluekiri BigData Team <bigdata@bluekiri.com>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as
 published by the Free Software Foundation, either version 3 of the
 License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

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
