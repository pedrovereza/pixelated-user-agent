define([],
function () {

  function withDisableOnFeature (featureFunction) {
    return function () {
      this.around('initialize', function (init) {
        if (featureFunction()) {
          init();
        }
      });
    };
  }

  return withDisableOnFeature;
});
