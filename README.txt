# The comparison runs in linux with python3 (with numpy) and matlab installed
# Install tools (Reluplex, Marabou, ReluVal, NNV)
chmod +x setup_tools.sh
./setup_tools.sh

# Run cases
# Subsets of input range of the property 1-4 are tested for a fast comparison. 
# Reluplex is not included since the property can't be easily adjusted in their code.
# Results are logged into the "logs" folder
# Comparison tables in latex are created for each property
chmod +x run_tools.sh
./run_tools.sh
