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
 * Main JS script.
 */

(function($){

  $.fn.showAlert = function(type, title, message) {

    let icon;
    switch (type) {
      case "error":
        icon = "ban";
        break;
      case "warning":
        icon = "warning";
        break;
      case "success":
        icon = "check";
        break;
      default:
        icon = "info"
    }

    let alert = $(Mustache.render($('#alert').html(), {
      type: type,
      title: title,
      message: message
    }));

    alert.appendTo(this);

    setTimeout(function() {
      $('[data-dismiss="alert"]', alert).trigger('click')
    }, 5000);

  }
})(jQuery);

let ST = {};
let ws;

ST.set = function(key, value) {
  if (typeof(Storage) !== "undefined") {
    localStorage.setItem(key, value)
  }
};

ST.get = function(key, value) {
  if (typeof(Storage) !== "undefined") {
    return localStorage.getItem(key)
  }
  return null
};

let SWHandler = {};
SWHandler.handle = function(ev) {
  try {
    const tick = JSON.parse(ev.data);
    const app = tick.application;
    const signal = $('[data-signal]').data("signal");
    if (signal === tick.signal) {
      const data = {
        ts: Date.parse(tick.ts),
        value: tick.agg_value,
        lower: tick.anomaly_results.value_lower_limit,
        upper: tick.anomaly_results.value_upper_limit
      };

      const len = sources[app].data.ts.length;
      sources[app].stream(data, len);
      if (tick.anomaly_results.is_anomaly > 0) {
        const anomaly_data = {
          ts: Date.parse(tick.ts),
          anomaly: tick.agg_value
        };
        const len = anomaly_sources[app].data.ts.length;
        anomaly_sources[app].stream(anomaly_data, len);
      }
      console.log("Event added");
    }
  } catch (error) {
    if (error.isPrototypeOf(TypeError)) {
      // Do nothing
    } else {
      console.log(error)
    }
  }
};

$(function(){

  // Ignore websockets
  Pace.options.ajax.trackWebSockets = false;
  Pace.options.ajax.ignoreURLs = ['json'];

  // Pace
  $(document).ajaxStart(function() {
    Pace.restart();
  }).ajaxStop(function() {
    Pace.stop();
  });

  // Active URL
  $('[data-uri="' + window.location.pathname + '"]').addClass("active").closest('.treeview').addClass('active');

  let body = $('body');
  body.on('collapsed.pushMenu',function(ev) {
    ST.set("sidebar", "collapsed")
  });

  body.on('expanded.pushMenu',function(ev) {
    ST.set("sidebar", "expanded")
  });

  if (ST.get("sidebar") !== null && ST.get("sidebar") === "collapsed") {
    $('body').addClass('sidebar-collapse')
  }

  // WebSocket
  function WSConnect() {
    interval = setInterval(function(){
      if (ws == null || (ws.readyState !== 1 && ws.readyState !== 0 && ws.readyState !== 2)) {
        try {
          ws = new WebSocket("ws://" +  window.location.href.match(/(http|https):\/\/([^\/]+)/)[2] + "/ws/");

          ws.onopen = function() {
            ws.send(JSON.stringify({ "op": "broadcast", "data": { "message": "I'm connected" } }));
            $('#ws-indicator').attr('title', "WS connected")
                              .find('.fa').removeClass('text-red').addClass('text-green');
            clearInterval(interval);
          };

          ws.onmessage = function(ev) {
            SWHandler.handle(ev);
          };

          ws.onclose = function(ev) {
            $('#ws-indicator').attr('title', "WS not connected").find('.fa').removeClass('text-green').addClass('text-red')
            WSConnect();
          };

        } catch (error) {
          console.log("Could not connect to WS")
        }
      }
    }, 1000)
  }

  WSConnect();

});