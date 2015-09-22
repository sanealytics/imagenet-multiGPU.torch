function createModel(nGPU)
    assert(nGPU == 1 or nGPU == 2, '1-GPU or 2-GPU supported for this net')
    local features
    if nGPU == 1 then
       features = nn.Concat(1)
    else
       require 'fbcunn'
       features = nn.ModelParallel(1)
    end

    -- load model from zoo
    require 'loadcaffe'

    local proto_name = 'deploy.prototxt'
    local model_name = 'nin_imagenet.caffemodel'
    local img_mean_name = 'ilsvrc_2012_mean.t7'
    local model_dir = 'models/nin/'

    local nin = loadcaffe.load(model_dir .. proto_name, model_dir .. model_name)

    local model = nn.Sequential()

    -- remove the classify part
    nin.modules[29] = nil 
    nin.modules[28] = nil 
    nin.modules[27] = nil 

    features:add(nin)

    local classifier = nn.Sequential()
    classifier:add(nn.View(256*6*6))
    classifier:add(nn.Dropout(0.5))
    classifier:add(nn.Linear(256*6*6, 4096))
    classifier:add(nn.Threshold(0, 1e-6))
    classifier:add(nn.Dropout(0.5))
    classifier:add(nn.Linear(4096, 4096))
    classifier:add(nn.Threshold(0, 1e-6))
    classifier:add(nn.Linear(4096, nClasses))
    classifier:add(nn.LogSoftMax())

--    local classifier = nn.Sequential()
--    classifier:add(nn.SpatialConvolutionMM(1024, nClasses, 1, 1, 1, 1, 0, 0))
--    classifier:add(nn.ReLU(true))
--    classifier:add(nn.SpatialAveragePooling(6, 6, 1, 1))
--
    -- Combine both to create final model
    local model = nn.Sequential():add(features):add(classifier)

    -- model.modules[1]:zeroGradParameters() -- don't change these weights yet, ideally just change the LR to very small

    return model

end

