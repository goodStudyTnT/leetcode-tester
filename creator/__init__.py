from creator.cpp_creator import CppCreator
from creator.golang_creator import GolangCreator

creator_factory = {
    CppCreator.code_type: CppCreator,
    GolangCreator.code_type: GolangCreator,
}
