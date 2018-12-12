describe('Emoji', function() {
  var emojis = {
        "wine_glass": "/static/emoji/img/wine_glass.png",
        "clock830": "/static/emoji/img/clock830.png",
        "water_buffalo": "/static/emoji/img/water_buffalo.png",
        "european_post_office": "/static/emoji/img/european_post_office.png",
        "mega": "/static/emoji/img/mega.png",
        "department_store": "/static/emoji/img/department_store.png",
        "four": "/static/emoji/img/four.png",
        "baby": "/static/emoji/img/baby.png",
        "gb": "/static/emoji/img/gb.png",
        "smoking": "/static/emoji/img/smoking.png"
      };

  describe('#setDataUrl', function() {
    it('should set the data url and return self', function() {
      expect(Emoji.setDataUrl('whatever')).toBe(Emoji);
    });
  });

  describe('#load', function() {
    var xhr, requests;

    beforeEach(function() {
      jasmine.Ajax.install();
      Emoji.clear();
    });
    afterEach(function() {
      jasmine.Ajax.uninstall();
    });
    it('should not raise objections loading an object', function() {
      Emoji.load(emojis);
    });

    it('should load from dataUrl if set and no data given', function() {

      Emoji.setDataUrl('whatever').load();
      var request = jasmine.Ajax.requests.mostRecent();
      request.respondWith({
        status: 200,
        type: 'application/json',
        responseText: '{"horray": "horray.png"}'
      });

      expect(request.method).toBe('GET');
      expect(request.url).toBe('whatever');
    });

    it('should load from localStorage if emojis exists', function() {
      localStorage.setItem('emojis', '{"Hello": "Hello.png"}');
      localStorage.setItem('emoji-version', Emoji.version());
      Emoji.load();

      expect(Emoji.get('Hello')).toBe('Hello.png');
    });

    it('should only load localStorage when emoji-version matches', function() {
      localStorage.setItem('emojis', '{"Hello": "Hello.png"}');
      localStorage.setItem('emoji-version', -1);
      Emoji.load();

      expect(Emoji.get('Hello')).toBe(undefined);
    });
  });

  describe('#get', function() {
    beforeEach(function() {
      Emoji.load(emojis);
    });

    it('should return the url for an existing emoji', function() {
      expect(Emoji.get('wine_glass')).toBe('/static/emoji/img/wine_glass.png');
    });

    it('should return undefined for a nonexisting emoji', function() {
      expect(Emoji.get('nonexistant_emoji')).toBe(undefined);
    });

    it('if no argument passed return all emoji names', function() {
      var keys = [];
      for(var k in emojis) keys.push(k);

      expect(Emoji.get()).toEqual(keys);
    });
  });

  describe('#replace', function() {
    beforeEach(function() {
      Emoji.load(emojis);
    });

    it('should return a string with no emojis unchanged', function() {
      expect(Emoji.replace('Hello.')).toBe('Hello.');
    });

    it('should return an existing emoji replaced to HTML', function() {
      expect(Emoji.replace(':wine_glass:'))
        .toBe('<img src="/static/emoji/img/wine_glass.png" ' +
              'alt="wine glass" class="emoji">');
    });

    it('should return several replaced emojis with HTML', function() {
      expect(Emoji.replace("Oh my it's late :clock830:, better ride my " +
                           ":water_buffalo: home."))
        .toBe('Oh my it\'s late <img src="/static/emoji/img/clock830.png" ' +
              'alt="clock830" class="emoji">, better ride my ' +
              '<img src="/static/emoji/img/water_buffalo.png" ' +
              'alt="water buffalo" class="emoji"> home.');
    });

    it('should do nothing with an invalid emoji', function() {
      expect(Emoji.replace(':takeiohmy:')).toBe(':takeiohmy:');
    });
  });

  describe('#clear', function() {
    it('should clear all data when called', function() {
      localStorage.setItem('emojis', 'something');
      localStorage.setItem('emoji-version', '1');
      Emoji.setDataUrl('meeow');

      Emoji.clear();

      expect(localStorage.getItem('emojis')).toBe(null);
      expect(localStorage.getItem('emoji-version')).toBe(null);
      expect(Emoji.dataUrl()).toBe(null);
    });
  });
});
