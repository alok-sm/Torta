'use strict';

describe('Service: bootbox', function () {

  // load the service's module
  beforeEach(module('ngPlayerApp'));

  // instantiate service
  var bootbox;
  beforeEach(inject(function (_bootbox_) {
    bootbox = _bootbox_;
  }));

  it('should do something', function () {
    expect(!!bootbox).toBe(true);
  });

});
