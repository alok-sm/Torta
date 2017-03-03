'use strict';

describe('Directive: screencast', function () {

  // load the directive's module
  beforeEach(module('ngPlayerApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<screencast></screencast>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the screencast directive');
  }));
});
