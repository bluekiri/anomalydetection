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
            f.handleEvent(ev);
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