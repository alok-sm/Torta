'use strict';

describe('Directive: appWindow', function () {

  // load the directive's module
  beforeEach(module('ngPlayerApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<app-window></app-window>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the appWindow directive');
  }));
});
