// Generated by CoffeeScript 1.3.3
(function() {

  define(['aloha', 'aloha/plugin', 'jquery', 'aloha/ephemera', 'ui/ui', 'ui/button'], function(Aloha, Plugin, jQuery, Ephemera, UI, Button) {
    var NEW_NOTE_TEMPLATE, enable;
    NEW_NOTE_TEMPLATE = '<div class="note">\n	<h2 class="title">Note Title</h2>\n	<p>Replace this with the body of the note</p>\n</div>';
    UI.adopt('insertNote', Button, {
      click: function(a, b, c) {
        var $newNote, range;
        range = Aloha.Selection.getRangeObject();
        $newNote = jQuery(NEW_NOTE_TEMPLATE);
        $newNote.addClass('aloha-new-note');
        GENTICS.Utils.Dom.insertIntoDOM($newNote, range, Aloha.activeEditable.obj);
        $newNote = Aloha.jQuery('.aloha-new-note');
        $newNote.removeClass('aloha-new-note');
        return enable($newNote);
      }
    });
    enable = function($note) {
      var $body, $title;
      $title = $note.children(':not(.aloha-block-handle)').first();
      if (!$title.is('.title')) {
        $title = jQuery('<h1 class="title"></h1>').prependTo($note);
      }
      $body = $note.find('.body');
      if (!$body[0]) {
        $body = jQuery('<div class="body"></div>');
        $note.children().not($title).appendTo($body);
      }
      $body.appendTo($note);
      $title.aloha();
      $body.aloha();
      return $note.alohaBlock();
    };
    return Aloha.bind('aloha-editable-activated', function(evt, props) {
      return props.editable.obj.find('.note').each(function(i, note) {
        return enable(jQuery(note));
      });
    });
  });

}).call(this);
