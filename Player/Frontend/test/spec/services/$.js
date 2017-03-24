'use strict';

describe('Service: $', function () {

  // load the service's module
  beforeEach(module('ngPlayerApp'));

  // instantiate service
  var $;
  beforeEach(inject(function (_$_) {
    $ = _$_;
  }));

  it('should do something', function () {
    expect(!!$).toBe(true);
  });

});
