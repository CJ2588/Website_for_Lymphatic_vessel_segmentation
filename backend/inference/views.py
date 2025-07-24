
import nibabel as nib
import torch
import torchvision.transforms as T
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

# Choose device

device = torch.device('cuda') if torch.cuda.is_available() else torch.device("cpu")


# Load model (ensure the path is correct)
model = torch.load('../../checkpoint_best.pth', map_location=device)
model.eval()



@api_view(['POST'])
@parser_classes([MultiPartParser])

def segment(request):
    file = request.FILES['image']
    image = nib.load('../../checkpoint_best.pth').get_fdata()
    transform = T.ToTensor()
    input_tensor = transform(image)
    if input_tensor.ndim != 4:
        input_tensor.unsqueeze(0)
    
    with torch.no_grad():
        output = model(input_tensor)[0]  # Adjust based on model output

    # Convert output to mask or JSON
    prediction = torch.argmax(output, dim=0).numpy().tolist()
    return Response({'mask': prediction})