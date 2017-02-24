'use strict';

describe('Directive: terminalCommand', function () {

  // load the directive's module
  beforeEach(module('ngPlayerApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<terminal-command></terminal-command>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the terminalCommand directive');
  }));
});
